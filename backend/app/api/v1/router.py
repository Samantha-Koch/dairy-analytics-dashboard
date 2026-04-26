from fastapi import APIRouter

from backend.app.api.v1.endpoints import health
from backend.app.api.v1.endpoints import Dashboard
from backend.app.api.v1.endpoints import Costs
from backend.app.api.v1.endpoints import DataUpload
from backend.app.api.v1.endpoints import MarketData
from backend.app.api.v1.endpoints import Production
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(costs.router, prefix="/costs", tags=["costs"])
api_router.include_router(data_upload.router, prefix="/data-upload", tags=["data-upload"])
api_router.include_router(market_data.router, prefix="/market-data", tags=["market-data"])
api_router.include_router(production.router, prefix="/production", tags=["production"])