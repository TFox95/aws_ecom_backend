from pydantic import BaseModel, List
from datetime import datetime
from typing import Optional


class Cart(BaseModel):
    id: int
    profile_id: int
    created_at: datetime
    items: Optional[List["Cart_Item"]]


class Cart_Item(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    image_url: str
    stock_quantity: int
