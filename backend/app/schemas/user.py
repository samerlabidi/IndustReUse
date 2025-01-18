from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    company_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MaterialResponse(BaseModel):
    id: int
    name: str
    industry: str
    quantity: float
    unit: str
    location: str
    condition: str
    description: Optional[str]
    status: str = "available"
    owner_id: Optional[int]

    class Config:
        orm_mode = True

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    location: Optional[str] = None
    condition: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    provider: Optional[str] = None 