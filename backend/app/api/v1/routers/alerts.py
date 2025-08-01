import uuid
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import AlertRead
from app.crud.alert_crud import alert
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[AlertRead])
async def list_alerts(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all alerts.
    """
    alerts = await alert.get_multi(db=db, skip=skip, limit=limit)
    return alerts

@router.get("/{alert_id}", response_model=AlertRead)
async def get_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Get a specific alert by its ID.
    """
    alert_fetched = await alert.get(db=db, id=alert_id)
    return alert_fetched