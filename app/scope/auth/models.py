from os import urandom

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from pydantic import EmailStr
from argon2 import PasswordHasher
from argon2.exceptions import (VerifyMismatchError,
                               InvalidHashError, VerificationError)
from datetime import datetime

from core.database import Base


class User(Base):

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True, index=True)
    email = Column(String(length=255), unique=True, index=True)
    password = Column(String(length=128))  # Store hashed password
    created_at = Column(DateTime, default=datetime.utcnow)
    disabled = Column(Boolean, default=False)
    profile = relationship("Profile", back_populates="user", lazy="joined")

    def __init__(cls, username: String, email: EmailStr, password: String):
        cls.username = username
        cls.email = email
        cls.encode_password(password)

    def encode_password(cls, password) -> None:
        ph = PasswordHasher(salt_len=16)
        cls.password = ph.hash(password=password, salt=urandom(16))

    def verify_password(cls, password) -> bool:
        ph = PasswordHasher()
        try:
            return ph.verify(hash=cls.password, password=password)
        except (VerifyMismatchError,
                InvalidHashError,
                VerificationError) as exc:
            print(str(exc))
            return False


class Profile(Base):

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)
    # Add other fields as needed (phone, etc.)
    user = relationship(User, back_populates="profile")
