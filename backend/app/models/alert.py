import uuid
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from .enums import AlertType, AlertSeverity

if TYPE_CHECKING:
    from .vehicle import Vehicle

class Alert(SQLModel, table=True):
    __tablename__ = "alerts"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    resolved: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    
    # Foreign Keys
    vehicle_id: uuid.UUID = Field(foreign_key="vehicles.id", index=True)
    
    # Relationships
    vehicle: "Vehicle" = Relationship(back_populates="alerts")