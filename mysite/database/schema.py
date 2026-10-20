from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    registered_date: datetime

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    product_name: str
    price: float
    description: Optional[str] = None

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    product_name: str
    price: float
    description: Optional[str] = None

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    order_date: datetime

    class Config:
        from_attributes = True