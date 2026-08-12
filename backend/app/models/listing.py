from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, JSON, Column
from datetime import datetime

class ListingBase(SQLModel):
    id: str = Field(primary_key=True)
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
    
    important_specifications: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    source_type: str = "demo"

class Listing(ListingBase, table=True):
    __tablename__ = "listings"

class ComparisonRecord(SQLModel, table=True):
    __tablename__ = "comparisons"
    
    id: str = Field(primary_key=True)
    query: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
