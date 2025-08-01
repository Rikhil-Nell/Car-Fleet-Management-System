import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.enums import AlertType, AlertSeverity

class AlertBase(BaseModel):
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    resolved: bool = False

class AlertCreate(AlertBase):
    vehicle_id: uuid.UUID

class AlertRead(AlertBase):
    id: uuid.UUID
    vehicle_id: uuid.UUID
    created_at: datetime