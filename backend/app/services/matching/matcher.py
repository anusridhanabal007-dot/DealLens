import re
from typing import Dict, Any, List, Tuple

class ProductMatcherEngine:
    """3-Level Hybrid Product Matching Engine"""

    @staticmethod
    def _clean_token_set(text: str) -> set:
        if not text:
            return set()
        clean = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = set(clean.split())
        # Remove common noisy stop words in e-commerce titles
        stop_words = {"the", "a", "an", "and", "or", "for", "with", "in", "by", "of", "to", "official", "original", "brand"}
        return tokens - stop_words

    def compare_attributes(self, listing_a: Dict[str, Any], listing_b: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Level 1: Strict Hard Constraints Check"""
        mismatches = []
        
        # 1. Brand Mismatch Check (e.g. Apple vs Samsung)
        brand_a = (listing_a.get("brand") or "").lower().strip()
        brand_b = (listing_b.get("brand") or "").lower().strip()
        if brand_a and brand_b and brand_a != brand_b:
            mismatches.append(f"Brand mismatch: '{listing_a.get('brand')}' vs '{listing_b.get('brand')}'")
            
        # 2. Model / Sub-model Mismatch Check (e.g. iPhone 15 vs iPhone 15 Pro, S24 vs S24 Ultra)
        model_a = (listing_a.get("model") or "").lower().strip()
        model_b = (listing_b.get("model") or "").lower().strip()
        if model_a and model_b and model_a != model_b:
            mismatches.append(f"Model mismatch: '{listing_a.get('model')}' vs '{listing_b.get('model')}'")

        # Title-level submodel modifier check (e.g. 'Pro', 'Pro Max', 'Plus', 'Ultra')
        title_a = (listing_a.get("product_name") or listing_a.get("raw_title") or "").lower()
        title_b = (listing_b.get("product_name") or listing_b.get("raw_title") or "").lower()

        modifiers = ["pro max", "pro", "plus", "ultra", "mini", "max"]
        for mod in modifiers:
            in_a = f" {mod} " in f" {title_a} " or title_a.endswith(f" {mod}")
            in_b = f" {mod} " in f" {title_b} " or title_b.endswith(f" {mod}")
            if in_a != in_b:
                mismatches.append(f"Model variant mismatch: '{mod}' in one title but not the other")
                break

        # 3. Storage Mismatch Check (e.g. 128GB vs 256GB)
        storage_a = (listing_a.get("storage") or "").upper().strip()
        storage_b = (listing_b.get("storage") or "").upper().strip()
        
        # If storage is missing in dict, extract from title
        if not storage_a:
            match_a = re.search(r'(\d+)[\s-]*(GB|TB)', title_a.upper())
            if match_a:
                storage_a = f"{match_a.group(1)}{match_a.group(2)}"
        if not storage_b:
            match_b = re.search(r'(\d+)[\s-]*(GB|TB)', title_b.upper())
            if match_b:
                storage_b = f"{match_b.group(1)}{match_b.group(2)}"

        if storage_a and storage_b and storage_a != storage_b:
            mismatches.append(f"Storage capacity mismatch: '{storage_a}' vs '{storage_b}'")

        # 4. RAM Mismatch Check (e.g. 8GB vs 16GB)
        ram_a = (listing_a.get("ram") or "").upper().strip()
        ram_b = (listing_b.get("ram") or "").upper().strip()
        if ram_a and ram_b and ram_a != ram_b:
            mismatches.append(f"RAM capacity mismatch: '{ram_a}' vs '{ram_b}'")

        passed_hard_constraints = len(mismatches) == 0
        return passed_hard_constraints, mismatches

    def calculate_title_similarity(self, title_a: str, title_b: str) -> float:
        """Level 2: Normalized Token Similarity"""
        tokens_a = self._clean_token_set(title_a)
        tokens_b = self._clean_token_set(title_b)
        
        if not tokens_a or not tokens_b:
            return 0.0
            
        intersection = tokens_a.intersection(tokens_b)
        union = tokens_a.union(tokens_b)
        
        return len(intersection) / len(union) if union else 0.0

    def match(self, listing_a: Dict[str, Any], listing_b: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate matching flow: Hard Constraints -> Attribute Similarity -> Confidence Score"""
        passed_hard, mismatches = self.compare_attributes(listing_a, listing_b)
        
        if not passed_hard:
            return {
                "same_product": False,
                "confidence": 0.1,
                "reason": f"Conflict in critical specifications: {', '.join(mismatches)}",
                "mismatched_attributes": mismatches
            }

        title_sim = self.calculate_title_similarity(
            listing_a.get("product_name", ""),
            listing_b.get("product_name", "")
        )

        # Attribute overlap score
        attr_matches = 0
        total_attrs = 0
        
        for key in ["brand", "model", "storage", "ram", "color"]:
            val_a = (listing_a.get(key) or "").lower()
            val_b = (listing_b.get(key) or "").lower()
            if val_a and val_b:
                total_attrs += 1
                if val_a == val_b:
                    attr_matches += 1
                    
        attr_score = (attr_matches / total_attrs) if total_attrs > 0 else 0.8
        
        # Weighted overall confidence
        confidence = round((title_sim * 0.5) + (attr_score * 0.5), 2)
        confidence = max(0.5, min(0.99, confidence))
        
        same_product = confidence >= 0.70
        reason = "Listings share identical core specifications and high title similarity" if same_product else "Partial match"
        
        return {
            "same_product": same_product,
            "confidence": confidence,
            "reason": reason,
            "mismatched_attributes": []
        }
