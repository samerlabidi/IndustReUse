from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class MaterialInfo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    quantity: float
    unit: str
    owner_id: int
    status: Optional[str] = 'available'
    
    model_config = ConfigDict(from_attributes=True)

class UserInfo(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    company_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class TransactionBase(BaseModel):
    material_id: int
    quantity: float
    message: Optional[str] = None
    delivery_method: Optional[str] = None
    delivery_date: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(BaseModel):
    id: int
    material_id: int
    from_owner_id: int
    to_owner_id: int
    quantity: float
    status: str
    message: Optional[str] = None
    delivery_method: Optional[str] = None
    delivery_date: Optional[str] = None
    created_at: datetime
    material: MaterialInfo
    from_user: UserInfo
    to_user: UserInfo
    
    model_config = ConfigDict(from_attributes=True)

class TransactionUpdate(BaseModel):
    status: str 