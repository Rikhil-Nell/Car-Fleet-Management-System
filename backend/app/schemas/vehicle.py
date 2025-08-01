import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from app.models.enums import RegistrationStatus


class VehicleBase(BaseModel):
    vin: str
    manufacturer: str
    model: str
    fleet_id: str
    owner_operator: str
    registration_status: Optional[RegistrationStatus] = RegistrationStatus.ACTIVE


class VehicleCreate(VehicleBase):
    pass 

class VehicleUpdate(BaseModel):
    fleet_id: Optional[str] = None
    owner_operator: Optional[str] = None
    registration_status: Optional[RegistrationStatus] = None


class VehicleRead(VehicleBase):
    id: uuid.UUID
    created_at: datetime
