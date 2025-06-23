from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# User Models
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Cook Profile Models
class CookProfileBase(BaseModel):
    name: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    delivery_radius: float = 5.0  # in miles

class CookProfileCreate(CookProfileBase):
    pass

class CookProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    delivery_radius: Optional[float] = None

class CookProfile(CookProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Menu Item Models
class MenuItemBase(BaseModel):
    title: str
    description: str
    price: float
    photo_url: Optional[str] = None
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    photo_url: Optional[str] = None
    is_available: Optional[bool] = None

class MenuItem(MenuItemBase):
    id: int
    cook_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Order Models
class OrderBase(BaseModel):
    menu_item_id: int
    quantity: int = 1
    special_instructions: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    special_instructions: Optional[str] = None

class Order(OrderBase):
    id: int
    buyer_id: int
    cook_id: int
    status: OrderStatus = OrderStatus.PENDING
    total_price: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Message Models
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    order_id: int

class Message(MessageBase):
    id: int
    order_id: int
    sender_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 