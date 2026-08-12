from typing import List, Dict, Any
from app.services.adapters.base import MarketplaceAdapter
from app.data.demo_products import get_demo_listings_for_query

class DemoMarketplaceAdapter(MarketplaceAdapter):
    def __init__(self, platform_name: str = "Demo Marketplace"):
        self._platform_name = platform_name

    @property
    def platform_name(self) -> str:
        return self._platform_name

    def search(self, query: str, cross_marketplace: bool = True) -> List[Dict[str, Any]]:
        return get_demo_listings_for_query(query, cross_marketplace=cross_marketplace)

    def get_listing(self, url_or_id: str) -> Dict[str, Any]:
        listings = get_demo_listings_for_query("iphone 15 128gb", cross_marketplace=True)
        for listing in listings:
            if listing["id"] == url_or_id:
                return listing
        return listings[0]

    def normalize_raw(self, raw_listing: Dict[str, Any]) -> Dict[str, Any]:
        # Ensure effective price is populated
        price = float(raw_listing.get("price", 0.0))
        delivery = float(raw_listing.get("delivery_fee", 0.0))
        raw_listing["effective_price"] = price + delivery
        return raw_listing
