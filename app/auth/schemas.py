
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


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
    profile: "UserProfile" or None  # Forward reference

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    address: str
    # Add other fields as needed

    class Config:
        orm_mode = True
