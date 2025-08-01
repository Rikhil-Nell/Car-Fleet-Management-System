import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import EngineStatus

class TelemetryCreate(BaseModel):
    vehicle_id: uuid.UUID
    latitude: float
    longitude: float
    speed: float
    engine_status: EngineStatus
    fuel_battery_level: float
    odometer_reading: float
    timestamp: datetime
    diagnostic_codes: str | None = None

class TelemetryRead(TelemetryCreate):
    id: uuid.UUID
    created_at: datetime