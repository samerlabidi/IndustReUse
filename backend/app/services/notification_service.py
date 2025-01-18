from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db
from app.models.models import Notification
from app.schemas.notification_schema import NotificationCreate, Notification as NotificationSchema

class NotificationService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def get_user_notifications(self, user_id: int) -> List[NotificationSchema]:
        notifications = self.db.query(Notification)\
            .filter(Notification.user_id == user_id)\
            .order_by(Notification.created_at.desc())\
            .all()
        return [NotificationSchema.from_orm(n) for n in notifications]
