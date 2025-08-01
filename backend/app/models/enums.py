from enum import Enum

class RegistrationStatus(str, Enum):
    ACTIVE = "Active"
    MAINTENANCE = "Maintenance"
    DECOMMISSIONED = "Decommissioned"

class EngineStatus(str, Enum):
    ON = "On"
    OFF = "Off"
    IDLE = "Idle"

class AlertType(str, Enum):
    SPEED_VIOLATION = "Speed Violation"
    LOW_FUEL_BATTERY = "Low Fuel/Battery"

class AlertSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"