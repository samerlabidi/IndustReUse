from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User
from app.core.security import verify_password

class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> User:
        try:
            print(f"Attempting to authenticate user: {email}")  # Debug log
            user = self.db.query(User).filter(User.email == email).first()
            
            if not user:
                print(f"User not found: {email}")  # Debug log
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )
            
            if not verify_password(password, user.hashed_password):
                print(f"Invalid password for user: {email}")  # Debug log
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )
            
            print(f"Authentication successful for user: {email}")  # Debug log
            return user
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")  # Debug log
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            ) 