
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from argon2 import PasswordHasher, hash_password
from datetime import datetime

from core.database import Base


class User(Base):

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True, index=True)
    email = Column(String(length=255), unique=True, index=True)
    password = Column(String(length=128))  # Store hashed password
    created_at = Column(DateTime, default=datetime.utcnow)
    disabled = Column(Boolean, default=False)
    profile = relationship("UserProfile", back_populates="user", lazy="joined")

    def __init__(cls, username: String, email: EmailStr, password: String):
        cls.username = username
        cls.email = email
        cls.encode_password(password)

    def encode_password(password) -> None:
        pass

    def verify_password() -> bool:
        pass


class UserProfile(Base):

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)
    # Add other fields as needed (phone, etc.)
    user = relationship("User", back_populates="profile")
