from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# ------------------ User ------------------

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^01[0-9]{9}$")
    role: Optional[str] = Field("user", pattern="^(user|admin)$")


class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^01[0-9]{9}$")
    role: Optional[str] = None

class UserOut(UserBase):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True


# ------------------ UserCredentials ------------------

class UserCredentialsBase(BaseModel):
    user_id: int
    hashed_password: str

class UserCredentialsCreate(BaseModel):
    user_id: int
    password: str = Field(..., min_length=6)

class UserCredentialsOut(BaseModel):
    id: int
    user_id: int
    hashed_password: str
    class Config:
        from_attributes = True
    

class UserLogin(BaseModel):
    email: str
    password: str



# ------------------ Category ------------------

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    class Config:
        from_attributes = True


# ------------------ Product ------------------

class ProductBase(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    # category_id: Optional[int] = None
    stock_quantity: int = Field(..., ge=0)
    category: Optional[CategoryOut] = None 

    class Config:
        from_attributes = True
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int]
    stock_quantity: Optional[int] = Field(None, ge=0)

class ProductOut(ProductBase):
    id: int
    name: str
    price: float
    stock_quantity: int
    category: Optional[CategoryOut] = None   # show category name too

    class Config:
        from_attributes = True


# ------------------ Order & OrderItem ------------------

class OrderItemBase(BaseModel):
    # order_id:int
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

# class OrderItemOut(OrderItemBase):
#     id: int
#     price: float
#     class Config:
#         from_attributes = True

class OrderItemOut(BaseModel):
    product_name: str
    quantity: int
    item_price: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int
    order_date: Optional[datetime] = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    user_id: int
    order_date: datetime
    items: list[OrderItemCreate]


class OrderOut(OrderBase):
    id: int
    order_date: datetime
    total_price: float   
    items: List[OrderItemOut]
    class Config:
        from_attributes = True
