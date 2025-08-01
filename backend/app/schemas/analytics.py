from pydantic import BaseModel, Field
from typing import Dict, List

class AlertSummary(BaseModel):
    count: int
    type: str
    severity: str

class AnalyticsSummary(BaseModel):
    active_vehicles_count: int
    inactive_vehicles_count: int
    average_fuel_level: float = Field(..., description="Average fuel/battery level across all vehicles.")
    total_distance_last_24h: float = Field(..., description="Total distance in km traveled by the fleet in the last 24 hours.")
    alert_summary: List[AlertSummary]