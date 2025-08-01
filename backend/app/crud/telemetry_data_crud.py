from app.crud.base_crud import CRUDBase
from app.models.telemetry_data import TelemetryData
from app.schemas.telemetry_data import TelemetryCreate, TelemetryRead

class CRUDTelemetryData(CRUDBase[TelemetryData, TelemetryCreate, TelemetryRead]):
    pass

telemetry_data = CRUDTelemetryData(TelemetryData)