from fastapi import APIRouter

from backend.app.api.v1.endpoints import health
from backend.app.api.v1.endpoints import dashboard

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
