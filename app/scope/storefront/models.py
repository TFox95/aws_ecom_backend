from sqlalchemy import (Column, Integer,
                        String, ForeignKey,
                        DateTime, Float)
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from core.database import Base
from scope.auth.models import Profile


class Product(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String)
    stock_quantity = Column(Integer, nullable=False, default=1)


class Cart(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    profile_id = Column(Integer, ForeignKey(Profile.id))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    items = relationship("Cart_Item", back_populates="cart", lazy="joined")
    cart = relationship("Cart",
                        backref=backref("profile",
                                        uselist=False,
                                        lazy="joined"))


class Cart_Item(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    cart_id = Column(Integer, ForeignKey(Cart.id))
    product_id = Column(Integer, ForeignKey(Product.id))
    quantity = Column(Integer)
    cart = relationship(Cart, back_populates="items")
    product = relationship(Product)


class Checkout(Base):
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    cart_id = Column(Integer, ForeignKey(Cart.id))
    order_total = Column(Float, nullable=False)
    shipping_address = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
