from typing import List, Dict, Any, Optional

class ValueScoringEngine:
    DEFAULT_WEIGHTS = {
        "price": 0.50,
        "seller": 0.25,
        "warranty": 0.15,
        "delivery": 0.10
    }

    def compute_effective_price(self, listing: Dict[str, Any]) -> float:
        price = float(listing.get("price", 0.0))
        delivery = float(listing.get("delivery_fee", 0.0))
        return round(price + delivery, 2)

    def validate_and_normalize_weights(self, custom_weights: Optional[Dict[str, float]]) -> Dict[str, float]:
        if not custom_weights:
            return dict(self.DEFAULT_WEIGHTS)

        keys = ["price", "seller", "warranty", "delivery"]
        weights_dict = {}
        for k in keys:
            if k in custom_weights and custom_weights[k] is not None:
                val = float(custom_weights[k])
                if val < 0:
                    raise ValueError(f"Weight for '{k}' cannot be negative (got {val}).")
                weights_dict[k] = val
            else:
                weights_dict[k] = self.DEFAULT_WEIGHTS[k]

        total_w = sum(weights_dict.values())

        # Decimal scale (approx 1.0) or Percentage scale (approx 100.0)
        if abs(total_w - 1.0) <= 0.05:
            return {k: weights_dict[k] / total_w for k in keys}
        elif abs(total_w - 100.0) <= 2.0:
            return {k: (weights_dict[k] / 100.0) / (total_w / 100.0) for k in keys}
        else:
            raise ValueError(
                f"Invalid weight configuration: Total weights must equal 100% or 1.0 (received total of {total_w})."
            )

    def calculate_scores(
        self,
        listings: List[Dict[str, Any]],
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Dict[str, float]]:
        if not listings:
            return {}

        weights = self.validate_and_normalize_weights(custom_weights)

        # Calculate effective prices first
        effective_prices = []
        for l in listings:
            eff_price = self.compute_effective_price(l)
            l["effective_price"] = eff_price
            effective_prices.append(eff_price)

        min_eff_price = min(effective_prices) if effective_prices else 1.0

        scores_map: Dict[str, Dict[str, float]] = {}

        for l in listings:
            l_id = l["id"]
            eff_price = l["effective_price"]

            # 1. Price Score (100 = lowest effective price)
            price_score = (min_eff_price / eff_price * 100.0) if eff_price > 0 else 100.0
            price_score = min(100.0, max(0.0, price_score))

            # 2. Seller Score (Fallback to 70 if rating is missing)
            rating = l.get("seller_rating")
            if rating is not None:
                seller_score = (float(rating) / 5.0) * 100.0
            else:
                seller_score = 70.0  # Fair fallback for missing rating
            seller_score = min(100.0, max(0.0, seller_score))

            # 3. Warranty Score (12 months = 100)
            warranty_mo = l.get("warranty_months") or 0
            warranty_score = min(100.0, (float(warranty_mo) / 12.0) * 100.0)

            # 4. Delivery Score
            delivery_fee = float(l.get("delivery_fee", 0.0))
            delivery_days = int(l.get("delivery_days", 3))
            
            fee_penalty = 0.0 if delivery_fee == 0 else min(30.0, (delivery_fee / min_eff_price) * 500)
            speed_score = max(50.0, 100.0 - (delivery_days * 10))
            delivery_score = max(0.0, speed_score - fee_penalty)

            # 5. Overall Weighted Score
            overall = (
                price_score * weights["price"] +
                seller_score * weights["seller"] +
                warranty_score * weights["warranty"] +
                delivery_score * weights["delivery"]
            )

            # Penalty for used condition when compared against new products
            if "used" in str(l.get("condition", "")).lower():
                overall *= 0.88

            scores_map[l_id] = {
                "price_score": round(price_score, 1),
                "seller_score": round(seller_score, 1),
                "warranty_score": round(warranty_score, 1),
                "delivery_score": round(delivery_score, 1),
                "overall_score": round(overall, 1)
            }

        return scores_map
