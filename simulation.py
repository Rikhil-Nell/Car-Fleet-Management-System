import requests
import time
import random
from datetime import datetime, timezone

API_BASE_URL = "http://127.0.0.1:8000/api/v1"
SIMULATION_INTERVAL_SECONDS = 30

def get_vehicles_from_api():
    """Fetches the list of all vehicles to simulate."""
    try:
        response = requests.get(f"{API_BASE_URL}/vehicles/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching vehicles: {e}")
        return []

def generate_fake_telemetry(vehicle):
    """Generates a single, realistic telemetry reading for a vehicle."""
    return {
        "vehicle_id": vehicle["id"],
        "latitude": round(random.uniform(17.3, 17.5), 6),
        "longitude": round(random.uniform(78.3, 78.6), 6),
        "speed": round(random.uniform(0, 120), 2),
        "engine_status": random.choice(["On", "Off", "Idle"]),
        "fuel_battery_level": round(random.uniform(10, 100), 2),
        "odometer_reading": round(random.uniform(1000, 200000), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "diagnostic_codes": None
    }

def run_simulation():
    """Main simulation loop."""
    print("--- Starting Vehicle Telemetry Simulator ---")
    while True:
        vehicles = get_vehicles_from_api()
        if not vehicles:
            print("No vehicles found to simulate. Retrying in 30 seconds...")
        else:
            print(f"Simulating telemetry for {len(vehicles)} vehicles...")
            for vehicle in vehicles:
                telemetry_data = generate_fake_telemetry(vehicle)
                try:
                    # Send data to the new telemetry endpoint
                    requests.post(f"{API_BASE_URL}/telemetry/", json=telemetry_data)
                    print(f"  - Sent telemetry for VIN: {vehicle['vin']}")
                except requests.exceptions.RequestException as e:
                    print(f"  - Failed to send telemetry for VIN {vehicle['vin']}: {e}")
        
        print(f"\n--- Waiting for {SIMULATION_INTERVAL_SECONDS} seconds... ---\n")
        time.sleep(SIMULATION_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_simulation()