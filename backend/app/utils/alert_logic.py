from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.alert_crud import alert
from app.schemas.alert import AlertCreate
from app.models import TelemetryData
from app.models.enums import AlertType, AlertSeverity
from app.core.config import settings

SPEED_LIMIT_KMH = settings.SPEED_LIMIT_KMH
LOW_FUEL_THRESHOLD_PERCENT = settings.LOW_FUEL_THRESHOLD_PERCENT
SPEEDING_STRIKE_LIMIT = settings.SPEEDING_STRIKE_LIMIT

SPEEDING_STRIKES = {}

async def check_telemetry_for_alerts(db: AsyncSession, telemetry: TelemetryData):
    """
    Checks a single telemetry data point for potential alerts.
    """
    await _check_for_low_fuel(db, telemetry)
    await _check_for_speeding(db, telemetry)


async def _check_for_low_fuel(db: AsyncSession, telemetry: TelemetryData):
    """Checks for low fuel and creates an alert if necessary."""
    if telemetry.fuel_battery_level < LOW_FUEL_THRESHOLD_PERCENT:
        alert_in = AlertCreate(
            vehicle_id=telemetry.vehicle_id,
            alert_type=AlertType.LOW_FUEL_BATTERY,
            severity=AlertSeverity.MEDIUM,
            message=f"Vehicle fuel level is critical: {telemetry.fuel_battery_level}%."
        )
        await alert.create(db=db, obj_in=alert_in)

async def _check_for_speeding(db: AsyncSession, telemetry: TelemetryData):
    """Checks for speeding using a 3-strike system."""
    vehicle_id = telemetry.vehicle_id

    if telemetry.speed > SPEED_LIMIT_KMH:
        current_strikes = SPEEDING_STRIKES.get(vehicle_id, 0) + 1
        SPEEDING_STRIKES[vehicle_id] = current_strikes

        if current_strikes >= SPEEDING_STRIKE_LIMIT:
            alert_in = AlertCreate(
                vehicle_id=vehicle_id,
                alert_type=AlertType.SPEED_VIOLATION,
                severity=AlertSeverity.HIGH,
                message=f"Vehicle exceeded speed limit. Current speed: {telemetry.speed} km/h."
            )
            await alert.create(db=db, obj_in=alert_in)
            SPEEDING_STRIKES[vehicle_id] = 0

    else:
        if SPEEDING_STRIKES.get(vehicle_id, 0) > 0:
            SPEEDING_STRIKES[vehicle_id] = 0
