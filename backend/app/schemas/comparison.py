from typing import Optional, List, Dict
from pydantic import BaseModel, Field, ConfigDict

class MatchRequest(BaseModel):
    listing_a: Dict
    listing_b: Dict

class MatchResponse(BaseModel):
    same_product: bool
    confidence: float
    reason: str
    mismatched_attributes: List[str] = Field(default_factory=list)

class ComparisonRequest(BaseModel):
    query: str
    cross_marketplace: bool = Field(default=True, alias="cross_platform")
    cross_platform: Optional[bool] = None
    weights: Optional[Dict[str, float]] = None

    model_config = ConfigDict(populate_by_name=True)

class RecommendationDetail(BaseModel):
    winner_listing_id: str
    overall_score: float
    confidence: float
    reasons: List[str]
    trade_offs: List[str] = Field(default_factory=list)
    ai_explanation: str
    ai_mode: str  # "LLM" or "Deterministic fallback"

class ComparisonResponse(BaseModel):
    id: str
    query: str
    canonical_product: str
    matched: bool
    match_confidence: float
    total_listings: int
    listings: List[Dict]
    scores: Dict[str, Dict[str, float]]  # listing_id -> scores map
    recommendation: RecommendationDetail
    normalized_specs: Dict[str, Dict[str, str]]
