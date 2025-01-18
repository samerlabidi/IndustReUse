from fastapi import APIRouter

api_router = APIRouter()

# Import the routers after creating api_router
from app.core.auth import router as auth_router
from app.api.materials import router as materials_router
from app.api.transactions import router as transactions_router
from app.api.analytics import router as analytics_router

# Include the routers
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(materials_router, tags=["materials"])
api_router.include_router(transactions_router, tags=["transactions"])
api_router.include_router(analytics_router, tags=["analytics"])
