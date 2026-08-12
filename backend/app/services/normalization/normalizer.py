import re
from typing import Dict, Any, Tuple

class NormalizationEngine:
    @staticmethod
    def normalize_storage(raw: Any) -> str:
        if not raw:
            return ""
        text = str(raw).strip().upper()
        # Find numeric digit and unit with optional hyphens/spaces
        match = re.search(r'(\d+)[\s-]*(GB|TB|GIGABYTE|GIGABYTES|G|GIGA)', text)
        if match:
            num, unit = match.group(1), match.group(2)
            if unit in ["TB"]:
                return f"{num}TB"
            return f"{num}GB"
        return text

    @staticmethod
    def normalize_ram(raw: Any) -> str:
        if not raw:
            return ""
        text = str(raw).strip().upper()
        match = re.search(r'(\d+)[\s-]*(GB|GIGABYTE|GIGABYTES|G)', text)
        if match:
            return f"{match.group(1)}GB"
        return text

    @staticmethod
    def normalize_warranty(raw: Any) -> Tuple[str, int]:
        if not raw:
            return ("No Warranty", 0)
        text = str(raw).strip().lower()
        
        # Check years
        match_yr = re.search(r'(\d+)\s*(year|yr|years|yrs)', text)
        if match_yr:
            years = int(match_yr.group(1))
            months = years * 12
            return (f"{months} months", months)
            
        # Check months
        match_mo = re.search(r'(\d+)\s*(month|mo|months|mos)', text)
        if match_mo:
            months = int(match_mo.group(1))
            return (f"{months} months", months)
            
        if "free" in text or "official" in text or "brand" in text:
            return ("12 months", 12)
            
        return (str(raw), 0)

    @staticmethod
    def normalize_delivery_fee(raw: Any) -> float:
        if raw is None:
            return 0.0
        if isinstance(raw, (int, float)):
            return float(raw)
        text = str(raw).strip().lower()
        if any(term in text for term in ["free", "₹0", "$0", "no fee", "no delivery fee", "zero"]):
            return 0.0
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if numbers:
            return float(numbers[0])
        return 0.0

    @staticmethod
    def normalize_condition(raw: Any) -> str:
        if not raw:
            return "New"
        text = str(raw).strip().lower()
        if any(term in text for term in ["new", "sealed", "brand new", "factory new"]):
            return "New"
        if any(term in text for term in ["used", "refurbished", "pre-owned", "like new", "renewed"]):
            return "Used - Like New"
        return "New"

    @staticmethod
    def normalize_brand(raw: Any) -> str:
        if not raw:
            return ""
        return str(raw).strip().title()

    @staticmethod
    def normalize_model(raw: Any) -> str:
        if not raw:
            return ""
        return str(raw).strip()

    @staticmethod
    def normalize_variant(raw: Any) -> str:
        if not raw:
            return ""
        return str(raw).strip().title()

    @staticmethod
    def normalize_color(raw: Any) -> str:
        if not raw:
            return ""
        return str(raw).strip().title()

    def normalize_listing(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(listing)
        
        normalized["brand"] = self.normalize_brand(listing.get("brand"))
        normalized["model"] = self.normalize_model(listing.get("model"))
        normalized["variant"] = self.normalize_variant(listing.get("variant"))
        normalized["color"] = self.normalize_color(listing.get("color"))
        normalized["storage"] = self.normalize_storage(listing.get("storage"))
        normalized["ram"] = self.normalize_ram(listing.get("ram"))
        
        # Warranty
        w_str, w_months = self.normalize_warranty(listing.get("warranty", ""))
        normalized["warranty_months"] = listing.get("warranty_months") or w_months
        normalized["warranty"] = w_str if not listing.get("warranty") else listing.get("warranty")
            
        # Delivery Fee
        normalized["delivery_fee"] = self.normalize_delivery_fee(listing.get("delivery_fee", 0.0))
        
        # Price & Effective Price
        price = float(listing.get("price", 0.0))
        delivery = normalized["delivery_fee"]
        normalized["effective_price"] = price + delivery
        
        # Condition
        normalized["condition"] = self.normalize_condition(listing.get("condition", "New"))
        
        return normalized
