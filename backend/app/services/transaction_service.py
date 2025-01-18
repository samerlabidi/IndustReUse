from typing import List, Optional
from sqlalchemy.orm import Session, joinedload, aliased
from fastapi import Depends, HTTPException, status
from app.db.database import get_db
from app.models.models import Transaction, Material, Notification, TransactionStatus, User
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse
from datetime import datetime

class TransactionService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def create_transaction(self, transaction_data: TransactionCreate, from_user_id: int) -> TransactionResponse:
        """Create a new transaction request"""
        try:
            # Verify material exists and has enough quantity
            material = self.db.query(Material).filter(Material.id == transaction_data.material_id).first()
            if not material:
                raise HTTPException(status_code=404, detail="Material not found")
            
            if material.quantity < transaction_data.quantity:
                raise HTTPException(status_code=400, detail="Requested quantity exceeds available amount")

            # Create new transaction
            transaction = Transaction(
                **transaction_data.model_dump(),
                from_owner_id=from_user_id,
                to_owner_id=material.owner_id,
                status=TransactionStatus.PENDING
            )
            
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            return TransactionResponse.model_validate(transaction)

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update_transaction_status(self, transaction_id: int, new_status: str, user_id: int) -> TransactionResponse:
        """Update transaction status"""
        try:
            transaction = self.db.query(Transaction)\
                .options(
                    joinedload(Transaction.material),
                    joinedload(Transaction.from_user),
                    joinedload(Transaction.to_user)
                )\
                .filter(Transaction.id == transaction_id)\
                .first()

            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            if not transaction.material:
                raise HTTPException(status_code=400, detail="Transaction has no associated material")

            # Authorization check
            if new_status == "cancelled":
                if transaction.from_owner_id != user_id:
                    raise HTTPException(status_code=403, detail="Not authorized to cancel this transaction")
            else:
                if transaction.to_owner_id != user_id:
                    raise HTTPException(status_code=403, detail="Not authorized to update this transaction")

            transaction.status = new_status
            self.db.commit()
            self.db.refresh(transaction)

            return TransactionResponse.model_validate(transaction)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Error updating transaction: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update transaction: {str(e)}"
            )

    async def get_user_transactions(self, user_id: int) -> List[TransactionResponse]:
        """Get all transactions for a user with related data"""
        try:
            # Create aliases for the User model for from_user and to_user
            FromUser = aliased(User)
            ToUser = aliased(User)

            # Query with proper aliases
            transactions = (
                self.db.query(Transaction)
                .join(Material)
                .join(FromUser, FromUser.id == Transaction.from_owner_id)
                .join(ToUser, ToUser.id == Transaction.to_owner_id)
                .options(
                    joinedload(Transaction.material),
                    joinedload(Transaction.from_user),
                    joinedload(Transaction.to_user)
                )
                .filter(
                    (Transaction.from_owner_id == user_id) | 
                    (Transaction.to_owner_id == user_id)
                )
                .all()
            )

            # Debug logging
            for t in transactions:
                print(f"Transaction {t.id}:")
                print(f"  Material: {t.material.name if t.material else 'None'}")
                print(f"  From User: {t.from_user.username if t.from_user else 'None'}")
                print(f"  To User: {t.to_user.username if t.to_user else 'None'}")

            # Convert to response models with validation
            responses = []
            for t in transactions:
                try:
                    response = TransactionResponse.model_validate(t)
                    responses.append(response)
                except Exception as e:
                    print(f"Error validating transaction {t.id}: {str(e)}")
                    continue

            return responses

        except Exception as e:
            print(f"Error fetching transactions: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch transactions: {str(e)}"
            )

    async def get_incoming_transactions(self, user_id: int) -> List[TransactionResponse]:
        """Get incoming transactions where user is the provider"""
        transactions = self.db.query(Transaction)\
            .options(
                joinedload(Transaction.material),
                joinedload(Transaction.from_user),
                joinedload(Transaction.to_user)
            )\
            .filter(Transaction.to_owner_id == user_id)\
            .all()
        return [TransactionResponse.model_validate(t) for t in transactions]

    async def get_outgoing_transactions(self, user_id: int) -> List[TransactionResponse]:
        """Get outgoing transactions where user is the requester"""
        transactions = self.db.query(Transaction)\
            .options(
                joinedload(Transaction.material),
                joinedload(Transaction.from_user),
                joinedload(Transaction.to_user)
            )\
            .filter(Transaction.from_owner_id == user_id)\
            .all()
        return [TransactionResponse.model_validate(t) for t in transactions]

    async def get_transaction_stats(self, user_id: int) -> dict:
        """Get transaction statistics for a user"""
        try:
            total = self.db.query(Transaction).filter(
                (Transaction.from_owner_id == user_id) | 
                (Transaction.to_owner_id == user_id)
            ).count()
            
            pending = self.db.query(Transaction).filter(
                (Transaction.from_owner_id == user_id) | 
                (Transaction.to_owner_id == user_id),
                Transaction.status == TransactionStatus.PENDING
            ).count()
            
            completed = self.db.query(Transaction).filter(
                (Transaction.from_owner_id == user_id) | 
                (Transaction.to_owner_id == user_id),
                Transaction.status == TransactionStatus.COMPLETED
            ).count()
            
            rejected = self.db.query(Transaction).filter(
                (Transaction.from_owner_id == user_id) | 
                (Transaction.to_owner_id == user_id),
                Transaction.status.in_([TransactionStatus.REJECTED, TransactionStatus.CANCELLED])
            ).count()
            
            return {
                "total": total,
                "pending": pending,
                "completed": completed,
                "rejected": rejected
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def complete_transaction(self, transaction_id: int, user_id: int) -> TransactionResponse:
        """Complete a transaction"""
        try:
            transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")
            
            # Verify user is authorized (must be the receiver)
            if transaction.to_owner_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to complete this transaction")

            # Can only complete accepted transactions
            if transaction.status != TransactionStatus.ACCEPTED.value:
                raise HTTPException(status_code=400, detail="Can only complete accepted transactions")

            transaction.status = TransactionStatus.COMPLETED.value
            
            # Create notification for the sender
            notification = Notification(
                title="Transaction Completed",
                type="transaction",
                message=f"Transaction #{transaction.id} has been completed",
                user_id=transaction.from_owner_id,
                read=False
            )
            self.db.add(notification)
            
            self.db.commit()
            self.db.refresh(transaction)
            return TransactionResponse.model_validate(transaction)

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions with related data"""
        try:
            transactions = self.db.query(Transaction)\
                .options(
                    joinedload(Transaction.material),
                    joinedload(Transaction.from_user),
                    joinedload(Transaction.to_user)
                )\
                .all()
            
            # Debug logging
            print("Raw transactions from DB:", transactions)
            
            # Verify material relationship
            for transaction in transactions:
                if not transaction.material:
                    print(f"Warning: Transaction {transaction.id} has no material")
                    
            return transactions
        except Exception as e:
            print("Error in get_all_transactions:", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def get_transaction(self, transaction_id: int):
        transaction = self.db.query(Transaction)\
            .options(
                joinedload(Transaction.material),
                joinedload(Transaction.from_user),
                joinedload(Transaction.to_user)
            )\
            .filter(Transaction.id == transaction_id)\
            .first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    def update_transaction_status(self, transaction_id: int, status: str):
        transaction = self.get_transaction(transaction_id)
        transaction.status = status
        self.db.commit()
        self.db.refresh(transaction)
        return self.get_transaction(transaction_id)  # Get fresh copy with all relationships 