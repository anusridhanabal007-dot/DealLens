from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class SpecificationSchema(BaseModel):
    storage: Optional[str] = None
    ram: Optional[str] = None
    color: Optional[str] = None
    display: Optional[str] = None
    processor: Optional[str] = None
    battery: Optional[str] = None
    camera: Optional[str] = None
    extra: Dict[str, Any] = Field(default_factory=dict)

class ListingSchema(BaseModel):
    id: str
    platform: str
    product_name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    variant: Optional[str] = None
    storage: Optional[str] = None
    ram: Optional[str] = None
    color: Optional[str] = None
    condition: str = "New"
    
    price: float
    currency: str = "INR"
    delivery_fee: float = 0.0
    effective_price: float = 0.0
    
    seller_name: Optional[str] = None
    seller_rating: Optional[float] = None
    seller_review_count: Optional[int] = None
    
    warranty: Optional[str] = None
    warranty_months: Optional[int] = 0
    return_policy: Optional[str] = None
    delivery_days: Optional[int] = 3
    availability: str = "In Stock"
    
    important_specifications: Dict[str, Any] = Field(default_factory=dict)
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    source_type: str = "demo"

class UserWeights(BaseModel):
    price: float = 0.50
    seller: float = 0.25
    warranty: float = 0.15
    delivery: float = 0.10

class ListingScoreDetail(BaseModel):
    listing_id: str
    price_score: float
    seller_score: float
    warranty_score: float
    delivery_score: float
    overall_score: float

class ExtractionRequest(BaseModel):
    raw_title: str
    raw_description: Optional[str] = ""
    raw_price: Optional[float] = None
    raw_seller: Optional[str] = None
    raw_specifications: Optional[str] = ""

class ExtractionResponse(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    storage: Optional[str] = None
    ram: Optional[str] = None
    color: Optional[str] = None
    condition: Optional[str] = "New"
    price: Optional[float] = None
    delivery_fee: Optional[float] = 0.0
    seller_rating: Optional[float] = None
    warranty_months: Optional[int] = None
    uncertain_fields: List[str] = Field(default_factory=list)
