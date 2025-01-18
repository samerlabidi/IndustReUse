from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    company_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)

    materials = relationship("Material", back_populates="owner")
    transactions_sent = relationship("Transaction", foreign_keys="[Transaction.from_owner_id]", back_populates="from_user")
    transactions_received = relationship("Transaction", foreign_keys="[Transaction.to_owner_id]", back_populates="to_user")
    notifications = relationship("Notification", back_populates="user")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    industry = Column(String)
    location = Column(String)
    condition = Column(String)
    status = Column(String, default='available')
    provider = Column(String)

    owner = relationship("User", back_populates="materials")
    transactions = relationship("Transaction", back_populates="material")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    from_owner_id = Column(Integer, ForeignKey("users.id"))
    to_owner_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Float)
    status = Column(String)
    message = Column(Text)
    delivery_method = Column(String)
    delivery_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    material = relationship("Material", back_populates="transactions")
    from_user = relationship("User", foreign_keys=[from_owner_id], back_populates="transactions_sent")
    to_user = relationship("User", foreign_keys=[to_owner_id], back_populates="transactions_received")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    message = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications") 