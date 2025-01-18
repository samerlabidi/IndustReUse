from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.services.analytics_service import AnalyticsService
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import Dict, Any

router = APIRouter()

@router.get("/analytics/stats", response_model=Dict[str, Any])
async def get_analytics_stats(
    current_user = Depends(get_current_user),
    service: AnalyticsService = Depends(lambda: AnalyticsService(next(get_db())))
) -> Dict[str, Any]:
    """Get analytics statistics"""
    return await service.get_stats() 