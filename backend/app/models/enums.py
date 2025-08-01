from enum import Enum

# Vehicle
class RegistrationStatus(str, Enum):
    ACTIVE = "Active"
    MAINTENANCE = "Maintenance"
    DECOMMISSIONED = "Decommissioned"

# Telemetry Data
class EngineStatus(str, Enum):
    ON = "On"
    OFF = "Off"
    IDLE = "Idle"

# Alert
class AlertType(str, Enum):
    SPEED_VIOLATION = "Speed Violation"
    LOW_FUEL_BATTERY = "Low Fuel/Battery"

class AlertSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"