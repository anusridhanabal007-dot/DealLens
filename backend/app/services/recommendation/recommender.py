import json
import httpx
from typing import List, Dict, Any, Optional
from app.config import settings

class RecommendationEngine:
    def determine_winner(
        self,
        listings: List[Dict[str, Any]],
        scores_map: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """Deterministically select winner and analyze key winning reasons & trade-offs."""
        if not listings or not scores_map:
            raise ValueError("No listings or scores provided for recommendation.")

        # Pick listing with highest overall_score
        winner_id = max(scores_map.keys(), key=lambda lid: scores_map[lid]["overall_score"])
        winner_listing = next(l for l in listings if l["id"] == winner_id)
        winner_scores = scores_map[winner_id]

        # Calculate min price and max seller rating among all listings
        all_eff_prices = [l["effective_price"] for l in listings]
        all_ratings = [l.get("seller_rating", 0.0) for l in listings if l.get("seller_rating") is not None]
        
        min_eff_price = min(all_eff_prices) if all_eff_prices else winner_listing["effective_price"]
        max_rating = max(all_ratings) if all_ratings else 4.0

        reasons = []
        trade_offs = []

        # 1. Price reason / trade-off
        if winner_listing["effective_price"] == min_eff_price:
            reasons.append(f"Lowest effective price at ₹{winner_listing['effective_price']:,.0f}")
        else:
            diff = winner_listing["effective_price"] - min_eff_price
            trade_offs.append(f"Price is ₹{diff:,.0f} higher than the cheapest listing, compensated by higher seller/warranty score")

        # 2. Delivery fee trade-off
        if winner_listing.get("delivery_fee", 0.0) > 0:
            trade_offs.append(f"Delivery costs ₹{winner_listing['delivery_fee']:,.0f}")
        else:
            reasons.append("Free delivery included")

        # 3. Seller rating reason / trade-off
        winner_rating = winner_listing.get("seller_rating", 0.0)
        if winner_rating and winner_rating >= max_rating:
            reasons.append(f"Highest seller rating of {winner_rating:.1f}★")
        elif winner_rating and winner_rating >= 4.5:
            reasons.append(f"Strong seller rating of {winner_rating:.1f}★")
        elif winner_rating:
            trade_offs.append(f"Seller rating is {winner_rating:.1f}★")

        # 4. Warranty reason
        w_mo = winner_listing.get("warranty_months", 0)
        if w_mo >= 12:
            reasons.append(f"Includes full {w_mo} months warranty")
        elif w_mo > 0:
            trade_offs.append(f"Shorter warranty period of {w_mo} months")

        # 5. Condition reason
        if winner_listing.get("condition") == "New":
            reasons.append("Brand new condition")
        else:
            trade_offs.append(f"Condition: {winner_listing.get('condition')}")

        return {
            "winner_listing_id": winner_id,
            "overall_score": winner_scores["overall_score"],
            "confidence": 0.94,
            "reasons": reasons,
            "trade_offs": trade_offs,
            "winner_listing": winner_listing
        }

    def generate_deterministic_explanation(
        self,
        winner_listing: Dict[str, Any],
        reasons: List[str],
        trade_offs: List[str],
        all_listings: List[Dict[str, Any]],
        overall_score: Optional[float] = None
    ) -> str:
        """Deterministic fact-based explanation fallback when LLM is unavailable."""
        score_display = f"{overall_score}/100" if overall_score is not None else "the highest"
        lines = [
            f"🏆 {winner_listing['product_name']} (Listing {winner_listing['id']}) is recommended as the Best Overall Deal.",
            "",
            f"It achieves {score_display} overall value score with an effective price of ₹{winner_listing['effective_price']:,.0f} and seller rating of {winner_listing.get('seller_rating', 'N/A')}★.",
            ""
        ]

        if reasons:
            lines.append("Key Advantages:")
            for r in reasons:
                lines.append(f"  • {r}")
            lines.append("")

        if trade_offs:
            lines.append("Trade-offs to consider:")
            for t in trade_offs:
                lines.append(f"  • {t}")
            lines.append("")

        other_count = len(all_listings) - 1
        lines.append(f"Outperformed {other_count} competing listing{'s' if other_count != 1 else ''} based on normalized price, seller reputation, delivery, and warranty parameters.")

        return "\n".join(lines)

    async def generate_ai_explanation(
        self,
        winner_info: Dict[str, Any],
        all_listings: List[Dict[str, Any]],
        scores_map: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """Generate final explanation using LLM if key is configured, else deterministic fallback."""
        winner_listing = winner_info["winner_listing"]
        reasons = winner_info["reasons"]
        trade_offs = winner_info["trade_offs"]

        if not settings.LLM_API_KEY:
            exp = self.generate_deterministic_explanation(winner_listing, reasons, trade_offs, all_listings, overall_score=winner_info.get("overall_score"))
            return {
                "ai_explanation": exp,
                "ai_mode": "Deterministic fallback"
            }

        prompt = f"""You are an expert e-commerce comparison analyst for DealLens AI.
Write a concise, polished, executive summary explaining why Listing '{winner_listing['id']}' ({winner_listing['product_name']}) won the Best Overall Deal.

Data:
Winner Effective Price: ₹{winner_listing['effective_price']}
Winner Seller Rating: {winner_listing.get('seller_rating')}★
Winner Warranty: {winner_listing.get('warranty')}
Winning Reasons: {json.dumps(reasons)}
Trade-offs: {json.dumps(trade_offs)}
Overall Score: {winner_info['overall_score']}/100

Format as 3 short paragraphs with emojis and bullet points. Be factual, concise, and trustworthy."""

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    f"{settings.LLM_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.LLM_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3
                    }
                )
                if response.status_code == 200:
                    exp_text = response.json()["choices"][0]["message"]["content"].strip()
                    return {
                        "ai_explanation": exp_text,
                        "ai_mode": "LLM"
                    }
        except Exception:
            pass

        # Fallback if API request fails
        exp = self.generate_deterministic_explanation(winner_listing, reasons, trade_offs, all_listings, overall_score=winner_info.get("overall_score"))
        return {
            "ai_explanation": exp,
            "ai_mode": "Deterministic fallback"
        }
