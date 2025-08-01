import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship, Column, TIMESTAMP
from .enums import EngineStatus

if TYPE_CHECKING:
    from .vehicle import Vehicle

class TelemetryData(SQLModel, table=True):
    __tablename__ = "telemetry_data"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    latitude: float
    longitude: float
    speed: float
    engine_status: EngineStatus
    fuel_battery_level: float
    odometer_reading: float
    diagnostic_codes: Optional[str] = Field(default=None)
    timestamp: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
    
    # Foreign Keys
    vehicle_id: uuid.UUID = Field(foreign_key="vehicles.id", index=True)
    
    # Relationships
    vehicle: "Vehicle" = Relationship(back_populates="telemetry_data")