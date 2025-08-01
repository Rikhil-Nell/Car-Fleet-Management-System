from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta, timezone

from app.schemas.analytics import AnalyticsSummary, AlertSummary
from app.models import Vehicle, TelemetryData, Alert

async def get_summary(db: AsyncSession) -> AnalyticsSummary:
    """
    Performs all database queries to calculate the analytics summary.
    """
    time_24_hours_ago = datetime.now(timezone.utc) - timedelta(hours=24)

    # Active vs. Inactive Vehicles Count
    total_vehicles_result = await db.exec(select(func.count(Vehicle.id)))
    total_vehicles_count = total_vehicles_result.one()

    active_vehicles_query = select(func.count(func.distinct(TelemetryData.vehicle_id))).where(
        TelemetryData.timestamp >= time_24_hours_ago
    )
    active_vehicles_result = await db.exec(active_vehicles_query)
    active_vehicles_count = active_vehicles_result.one()
    inactive_vehicles_count = total_vehicles_count - active_vehicles_count

    # Average Fuel Level (from latest reading of each vehicle)
    latest_telemetry_sq = select(
        TelemetryData.vehicle_id,
        func.max(TelemetryData.timestamp).label("max_ts")
    ).group_by(TelemetryData.vehicle_id).alias("latest_telemetry_sq")

    avg_fuel_query = select(func.avg(TelemetryData.fuel_battery_level)).join(
        latest_telemetry_sq,
        (TelemetryData.vehicle_id == latest_telemetry_sq.c.vehicle_id) &
        (TelemetryData.timestamp == latest_telemetry_sq.c.max_ts)
    )
    avg_fuel_result = await db.exec(avg_fuel_query)
    average_fuel_level = avg_fuel_result.one_or_none() or 0.0

    # Total Distance Traveled by Fleet in Last 24 Hours
    distance_subquery = select(
        (func.max(TelemetryData.odometer_reading) - func.min(TelemetryData.odometer_reading)).label("distance_traveled")
    ).where(TelemetryData.timestamp >= time_24_hours_ago).group_by(TelemetryData.vehicle_id).alias("distance_subquery")
    
    total_distance_query = select(func.sum(distance_subquery.c.distance_traveled))
    total_distance_result = await db.exec(total_distance_query)
    total_distance_last_24h = total_distance_result.one_or_none() or 0.0

    # Alert Summary
    alert_summary_query = select(
        func.count(Alert.id), Alert.alert_type, Alert.severity
    ).group_by(Alert.alert_type, Alert.severity)
    alert_summary_result = await db.exec(alert_summary_query)
    alert_summary_rows = alert_summary_result.all()
    alert_summary = [AlertSummary(count=count, type=type, severity=severity) for count, type, severity in alert_summary_rows]

    return AnalyticsSummary(
        active_vehicles_count=active_vehicles_count,
        inactive_vehicles_count=inactive_vehicles_count,
        average_fuel_level=round(average_fuel_level, 2),
        total_distance_last_24h=round(total_distance_last_24h, 2),
        alert_summary=alert_summary,
    )