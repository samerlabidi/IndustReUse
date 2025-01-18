from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.services.transaction_service import TransactionService
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse, TransactionUpdate
from typing import List
from pydantic import BaseModel

router = APIRouter()

class TransactionStats(BaseModel):
    total: int
    pending: int
    completed: int
    rejected: int

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Create a new transaction request"""
    return await service.create_transaction(transaction, current_user.id)

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_user_transactions(
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Get all transactions for the current user"""
    return await service.get_user_transactions(current_user.id)

@router.get("/transactions/stats", response_model=TransactionStats)
async def get_transaction_stats(
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Get transaction statistics for the current user"""
    return await service.get_transaction_stats(current_user.id)

@router.get("/transactions/incoming", response_model=List[TransactionResponse])
async def get_incoming_transactions(
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Get incoming transaction requests"""
    return await service.get_incoming_transactions(current_user.id)

@router.get("/transactions/outgoing", response_model=List[TransactionResponse])
async def get_outgoing_transactions(
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Get outgoing transaction requests"""
    return await service.get_outgoing_transactions(current_user.id)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Get a specific transaction"""
    return await service.get_transaction(transaction_id, current_user.id)

@router.patch("/api/transactions/{transaction_id}/status", response_model=TransactionResponse)
async def update_transaction_status(
    transaction_id: int,
    status: str,
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Update transaction status"""
    return await service.update_transaction_status(transaction_id, status, current_user.id)

@router.get("/transactions/{transaction_id}/history")
async def get_transaction_history(
    transaction_id: int,
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Get transaction history"""
    return await service.get_transaction_history(transaction_id, current_user.id)

@router.post("/transactions/{transaction_id}/complete", response_model=TransactionResponse)
async def complete_transaction(
    transaction_id: int,
    current_user = Depends(get_current_user),
    service: TransactionService = Depends()
):
    """Complete a transaction"""
    return await service.complete_transaction(transaction_id, current_user.id) 