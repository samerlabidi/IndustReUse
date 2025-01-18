from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.models.models import Base
from app.api import api_router
from app.core.auth import router as auth_router
from app.api.materials import router as materials_router
from app.api.transactions import router as transactions_router
from app.api.notification import router as notifications_router
from app.api.analytics import router as analytics_router
from fastapi.responses import JSONResponse

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(materials_router, prefix="/api", tags=["materials"])
app.include_router(transactions_router, prefix="/api", tags=["transactions"])
app.include_router(notifications_router, prefix="/api", tags=["notifications"])
app.include_router(analytics_router, prefix="/api", tags=["analytics"])

# Add error handling
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    print(f"Internal Server Error: {str(exc)}")  # Add logging
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )