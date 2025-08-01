import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.vehicle_crud import vehicle
from app.schemas import VehicleCreate, VehicleRead, VehicleUpdate
from app.api import deps
from app.models import Vehicle

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VehicleRead)
async def create_vehicle(*, db: AsyncSession = Depends(deps.get_db), vehicle_in: VehicleCreate):
    """
    Create a new vehicle.
    """
    existing_vehicle = await vehicle.get_by_vin(db=db, vin=vehicle_in.vin)
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A vehicle with this VIN already exists.",
        )
    new_vehicle = await vehicle.create(db=db, obj_in=vehicle_in)
    return new_vehicle


@router.get("/", response_model=List[VehicleRead])
async def list_vehicles(
    db: AsyncSession = Depends(deps.get_db),
    vin: str = None,
    manufacturer: str = None,
    fleet_id: str = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    List and query vehicles with optional filters.
    """
    query = select(Vehicle)
    if vin:
        query = query.where(Vehicle.vin == vin)
    if manufacturer:
        query = query.where(Vehicle.manufacturer == manufacturer)
    if fleet_id:
        query = query.where(Vehicle.fleet_id == fleet_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.exec(query)
    vehicles = result.all()
    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle(
    *,
    db: AsyncSession = Depends(deps.get_db),
    vehicle_id: uuid.UUID,
):
    """
    Get a single vehicle by its ID.
    """
    vehicle_fetched = await vehicle.get(db=db, id=vehicle_id)
    if not vehicle_fetched:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )
    return vehicle_fetched


@router.patch("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(
    *,
    db: AsyncSession = Depends(deps.get_db),
    vehicle_id: uuid.UUID,
    vehicle_in: VehicleUpdate,
):
    """
    Update a vehicle's details.
    """
    db_vehicle = await vehicle.get(db=db, id=vehicle_id)
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )
    updated_vehicle = await vehicle.update(
        db=db, db_obj=db_vehicle, obj_in=vehicle_in
    )
    return updated_vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    *,
    db: AsyncSession = Depends(deps.get_db),
    vehicle_id: uuid.UUID,
):
    """
    Delete a vehicle.
    """
    vehicle_fetched = await vehicle.get(db=db, id=vehicle_id)
    if not vehicle_fetched:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found.",
        )
    await vehicle.remove(db=db, id=vehicle_id)
    return