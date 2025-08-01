from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import select, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.telemetry_data_crud import telemetry_data
from app.schemas.telemetry_data import TelemetryCreate, TelemetryRead
from app.api import deps
from app.models import TelemetryData
from app.models.enums import EngineStatus

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TelemetryRead)
async def receive_telemetry(*, db: AsyncSession = Depends(deps.get_db), telemetry_in: TelemetryCreate):
    """
    Receive and store a new telemetry data point.
    """
    new_telemetry = await telemetry_data.create(db=db, obj_in=telemetry_in)
    return new_telemetry

@router.get("/", response_model=List[TelemetryRead])
async def list_telemetry(
    db: AsyncSession = Depends(deps.get_db),
    speed: float | None = None,
    engine_status: EngineStatus | None = None,
    fuel_battery_level: float | None = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    List and query telemetry data with optional filters.
    """
    query = select(TelemetryData).order_by(TelemetryData.timestamp.desc())

    if speed is not None:
        query = query.where(TelemetryData.speed == speed)
    if engine_status is not None:
        query = query.where(TelemetryData.engine_status == engine_status)
    if fuel_battery_level is not None:
        query = query.where(TelemetryData.fuel_battery_level == fuel_battery_level)
    
    query = query.offset(skip).limit(limit)
    result = await db.exec(query)
    telemetry_list = result.all()
    return telemetry_list