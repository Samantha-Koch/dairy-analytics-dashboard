from fastapi import APIRouter

from backend.app.api.v1.endpoints import health
from backend.app.api.v1.endpoints import dashboard
from backend.app.api.v1.endpoints import Costs
from backend.app.api.v1.endpoints import DataUpload
from backend.app.api.v1.endpoints import MarketData
from backend.app.api.v1.endpoints import Production
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(Costs.router, prefix="/costs", tags=["costs"])
api_router.include_router(DataUpload.router, prefix="/dataupload", tags=["upload"])
api_router.include_router(MarketData.router, prefix="/marketdata", tags=["marketdata"])
api_router.include_router(Production.router, prefix="/production", tags=["production"])