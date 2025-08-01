from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate

class CRUDVehicle(CRUDBase[Vehicle, VehicleCreate, VehicleUpdate]):
    """
    CRUD methods for Vehicle, inheriting from CRUDBase.
    Add any vehicle-specific database methods here.
    """
    async def get_by_vin(self, db: AsyncSession, *, vin: str) -> Vehicle | None:
        """
        Get a single vehicle by its Vehicle Identification Number (VIN).
        """
        query = select(Vehicle).where(Vehicle.vin == vin)
        result = await db.exec(query)
        return result.first()

vehicle = CRUDVehicle(Vehicle)