
from pydantic import BaseModel, Field, EmailStr, List
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field(min_length=3, max_length=128)
    username: str = Field(min_length=3, max_length=50)
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    disabled: bool
    profile: Optional["Profile"]  # Forward reference

    class Config:
        orm_mode = True


class Profile(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    address: str
    # Add other fields as needed
    cart: Optional["Cart"]

    class Config:
        orm_mode = True


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
