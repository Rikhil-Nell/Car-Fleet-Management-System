import uuid
from typing import List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship, Column, String
from .enums import RegistrationStatus

if TYPE_CHECKING:
    from .telemetry_data import TelemetryData
    from .alert import Alert

class Vehicle(SQLModel, table=True):
    __tablename__ = "vehicles"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    vin: str = Field(sa_column=Column(String, index=True, unique=True))
    manufacturer: str
    model: str
    fleet_id: str = Field(index=True)
    owner_operator: str
    registration_status: RegistrationStatus = Field(default=RegistrationStatus.ACTIVE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    telemetry_data: List["TelemetryData"] = Relationship(back_populates="vehicle")
    alerts: List["Alert"] = Relationship(back_populates="vehicle")