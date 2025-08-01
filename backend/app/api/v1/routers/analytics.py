from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas.analytics import AnalyticsSummary
from app.utils import analytics_logic

router = APIRouter()

@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(db: AsyncSession = Depends(deps.get_db)):
    """
    Retrieve a summary of fleet analytics.
    """
    summary = await analytics_logic.get_summary(db=db)
    return summary