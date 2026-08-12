import uuid
from typing import Dict, Any, List, Optional
from sqlmodel import Session

from app.services.adapters.demo_adapters import DemoMarketplaceAdapter
from app.services.normalization.normalizer import NormalizationEngine
from app.services.matching.matcher import ProductMatcherEngine
from app.services.scoring.scorer import ValueScoringEngine
from app.services.recommendation.recommender import RecommendationEngine
from app.models.listing import ComparisonRecord
from app.database import engine

class ComparisonService:
    def __init__(self):
        self.adapter = DemoMarketplaceAdapter()
        self.normalizer = NormalizationEngine()
        self.matcher = ProductMatcherEngine()
        self.scorer = ValueScoringEngine()
        self.recommender = RecommendationEngine()

    async def compare_query(
        self,
        query: str,
        cross_marketplace: bool = True,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        # 1. Collect raw listings from marketplace adapter
        raw_listings = self.adapter.search(query, cross_marketplace=cross_marketplace)

        # 2. Normalize specifications and calculate effective prices
        normalized_listings = [self.normalizer.normalize_listing(l) for l in raw_listings]

        # 3. Match listings to verify product consistency across listings
        matched_results = []
        if len(normalized_listings) > 1:
            base_l = normalized_listings[0]
            for other_l in normalized_listings[1:]:
                m_res = self.matcher.match(base_l, other_l)
                matched_results.append(m_res)

        all_matched = all(m["same_product"] for m in matched_results) if matched_results else True
        match_confidence = (
            round(sum(m["confidence"] for m in matched_results) / len(matched_results), 2)
            if matched_results else 0.96
        )

        # 4. Deterministic Value Scoring
        scores_map = self.scorer.calculate_scores(normalized_listings, custom_weights)

        # 5. Recommendation winner determination
        rec_detail = self.recommender.determine_winner(normalized_listings, scores_map)

        # 6. AI Explanation Generation
        ai_res = await self.recommender.generate_ai_explanation(rec_detail, normalized_listings, scores_map)

        # Build normalized specification comparison matrix
        spec_matrix = {}
        for l in normalized_listings:
            spec_matrix[l["id"]] = {
                "storage": l.get("storage") or "N/A",
                "ram": l.get("ram") or "N/A",
                "color": l.get("color") or "N/A",
                "condition": l.get("condition") or "New",
                "warranty": l.get("warranty") or "1 Year",
                "delivery": f"₹{l['delivery_fee']:,.0f}" if l['delivery_fee'] > 0 else "Free"
            }

        comparison_id = str(uuid.uuid4())[:8]

        response_payload = {
            "id": comparison_id,
            "query": query,
            "canonical_product": normalized_listings[0]["product_name"],
            "matched": all_matched,
            "match_confidence": match_confidence,
            "total_listings": len(normalized_listings),
            "listings": normalized_listings,
            "scores": scores_map,
            "recommendation": {
                "winner_listing_id": rec_detail["winner_listing_id"],
                "overall_score": rec_detail["overall_score"],
                "confidence": rec_detail["confidence"],
                "reasons": rec_detail["reasons"],
                "trade_offs": rec_detail["trade_offs"],
                "ai_explanation": ai_res["ai_explanation"],
                "ai_mode": ai_res["ai_mode"]
            },
            "normalized_specs": spec_matrix
        }

        # Save to database asynchronously or via session
        try:
            with Session(engine) as session:
                rec = ComparisonRecord(
                    id=comparison_id,
                    query=query,
                    data=response_payload
                )
                session.add(rec)
                session.commit()
        except Exception:
            pass  # DB write optional for non-blocking demo

        return response_payload

    def get_comparison(self, comparison_id: str) -> Optional[Dict[str, Any]]:
        try:
            with Session(engine) as session:
                rec = session.get(ComparisonRecord, comparison_id)
                if rec:
                    return rec.data
        except Exception:
            pass
        return None
