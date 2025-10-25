from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, DateTime,
    CheckConstraint, Index
)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100))
    phone = Column(String(11), unique=True)
    role = Column(String(50), default="user")  # 'user' or 'admin'

    # One-to-one with credentials  every user have only one account
    credential = relationship("UserCredential", back_populates="user", uselist=False)
    # One-to-many with orders   every user can order different times
    orders = relationship("Order", back_populates="user")
    
    @property
    def email(self):
        return self.credential.email if self.credential else None
    
    __table_args__ = (
        CheckConstraint("phone REGEXP '^01[0-9]{9}$'", name="valid_phone"),
    )

class UserCredential(Base):
    __tablename__ = "UserCredentials"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    user = relationship("User", back_populates="credential")



class Category(Base):
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # One-to-many with Products   every category have many products
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "Products" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("Category.id", ondelete="SET NULL"))
    stock_quantity = Column(Integer, nullable=False, default=0)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    
    __table_args__ = (
        CheckConstraint("price > 0", name="check_price_positive"),
        CheckConstraint("stock_quantity >= 0", name="check_stock_nonnegative"),
        Index("idx_product_name", "name"),
    )

class Order(Base):
    __tablename__ = "Orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float, default=0)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
  

class OrderItem(Base):
    __tablename__ = "OrderItems"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("Products.id", ondelete="SET NULL"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("price >= 0", name="check_orderitem_price_nonnegative"),
    )