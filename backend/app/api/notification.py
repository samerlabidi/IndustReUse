from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.notification_schema import Notification, NotificationCreate
from app.services.notification_service import NotificationService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[Notification])
async def get_notifications(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = NotificationService(db)
    return await service.get_user_notifications(current_user.id)

@router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user = Depends(get_current_user),
    notification_service: NotificationService = Depends()
):
    return await notification_service.mark_as_read(notification_id, current_user.id)

@router.patch("/read-all")
async def mark_all_as_read(
    current_user = Depends(get_current_user),
    notification_service: NotificationService = Depends()
):
    return await notification_service.mark_all_as_read(current_user.id)

@router.delete("/clear-all")
async def clear_all_notifications(
    current_user = Depends(get_current_user),
    notification_service: NotificationService = Depends()
):
    return await notification_service.clear_all(current_user.id)

@router.get("/unread-count")
async def get_unread_count(
    current_user = Depends(get_current_user),
    notification_service: NotificationService = Depends()
):
    return await notification_service.get_unread_count(current_user.id)