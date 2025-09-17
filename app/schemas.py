from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# ===== Users =====
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserOut(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)

# ===== Sellers =====
class SellerBase(BaseModel):
    name: str
    email: EmailStr

class SellerCreate(SellerBase):
    pass

class SellerOut(SellerBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SellerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# ===== Products =====
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category: str
    seller_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    seller_id: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ===== Orders =====
class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = 1

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemIn]

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemOut]
    class Config:
        from_attributes = True
class OrderItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    items: Optional[List[OrderItemUpdate]] = None
