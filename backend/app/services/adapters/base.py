from abc import ABC, abstractmethod
from typing import List, Dict, Any

class MarketplaceAdapter(ABC):
    @property
    @abstractmethod
    def platform_name(self) -> str:
        pass
        
    @abstractmethod
    def search(self, query: str, cross_marketplace: bool = True) -> List[Dict[str, Any]]:
        """Search marketplace for listings matching query."""
        pass

    @abstractmethod
    def get_listing(self, url_or_id: str) -> Dict[str, Any]:
        """Fetch raw listing details by ID or URL."""
        pass

    @abstractmethod
    def normalize_raw(self, raw_listing: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw listing into canonical schema."""
        pass
