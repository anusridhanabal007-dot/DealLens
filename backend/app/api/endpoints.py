from fastapi import APIRouter, HTTPException, Query, Body
from typing import Dict, Any, List, Optional
from app.schemas.comparison import ComparisonRequest, ComparisonResponse, MatchRequest, MatchResponse
from app.schemas.listing import ExtractionRequest, ExtractionResponse
from app.services.comparison_service import ComparisonService
from app.services.extraction.extractor import ExtractionEngine
from app.services.matching.matcher import ProductMatcherEngine
from app.data.demo_products import DEMO_QUERIES

router = APIRouter()
comparison_service = ComparisonService()
extraction_engine = ExtractionEngine()
matcher_engine = ProductMatcherEngine()

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "DealLens AI Comparison Engine", "version": "1.0.0"}

@router.get("/demo-queries")
def get_demo_queries() -> List[str]:
    return DEMO_QUERIES

@router.post("/search")
def search_listings(query: str = Query(...)):
    raw_listings = comparison_service.adapter.search(query)
    return {
        "query": query,
        "count": len(raw_listings),
        "source": "Demo Marketplace Data",
        "listings": raw_listings
    }

@router.post("/compare", response_model=ComparisonResponse)
async def compare_listings(req: ComparisonRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")
    
    is_cross = req.cross_platform if req.cross_platform is not None else req.cross_marketplace
    result = await comparison_service.compare_query(
        query=req.query.strip(),
        cross_marketplace=is_cross,
        custom_weights=req.weights
    )
    return result

@router.post("/extract", response_model=ExtractionResponse)
async def extract_listing_info(req: ExtractionRequest):
    res = await extraction_engine.extract_structured(
        raw_title=req.raw_title,
        raw_description=req.raw_description or "",
        raw_price=req.raw_price
    )
    return res

@router.post("/match", response_model=MatchResponse)
def match_listings(req: MatchRequest):
    res = matcher_engine.match(req.listing_a, req.listing_b)
    return res

@router.get("/comparisons/{comparison_id}")
def get_stored_comparison(comparison_id: str):
    res = comparison_service.get_comparison(comparison_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Comparison ID '{comparison_id}' not found.")
    return res
