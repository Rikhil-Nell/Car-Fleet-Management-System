from fastapi import APIRouter
from app.api.v1.routers import vehicles, telemetry_data
from app.api.v1.routers import alerts

api_router = APIRouter()
api_router.include_router(router=vehicles.router, prefix="/vehicles", tags=["Vehicles"])
# The other two routers will be created later, this is just for structure
# api_router.include_router(router=telemetry_data.router, prefix="/telemetry", tags=["Telemetry"])
# api_router.include_router(router=alert.router, prefix="/alerts", tags=["Alerts"])