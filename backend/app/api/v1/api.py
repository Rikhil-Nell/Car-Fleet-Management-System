from fastapi import APIRouter
from app.api.v1.routers import vehicles, telemetry_data
from app.api.v1.routers import alerts
from app.api.v1.routers import analytics

api_router = APIRouter()
api_router.include_router(router=vehicles.router, prefix="/vehicles", tags=["Vehicles"])
api_router.include_router(router=telemetry_data.router, prefix="/telemetry", tags=["Telemetry"])
api_router.include_router(router=alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(router=analytics.router, prefix="/analytics", tags=["Analytics"])