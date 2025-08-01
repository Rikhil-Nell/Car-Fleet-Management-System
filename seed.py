import requests
import json

# The base URL of your running FastAPI application
BASE_URL = "http://127.0.0.1:8000"
API_V1_STR = "/api/v1"

def seed_data():
    """
    Sends POST requests to the /vehicles/ endpoint to create initial data.
    """
    endpoint = f"{BASE_URL}{API_V1_STR}/vehicles/"
    
    # A list of vehicle data to create
    vehicles_to_create = [
        {
            "vin": "VIN_TESLA_123456789",
            "manufacturer": "Tesla",
            "model": "Model Y",
            "fleet_id": "Corporate",
            "owner_operator": "Alice Johnson",
            "registration_status": "Active"
        },
        {
            "vin": "VIN_FORD_987654321",
            "manufacturer": "Ford",
            "model": "F-150 Lightning",
            "fleet_id": "Rental",
            "owner_operator": "Bob Williams",
            "registration_status": "Active"
        },
        {
            "vin": "VIN_BMW_ABC123DEF",
            "manufacturer": "BMW",
            "model": "i4",
            "fleet_id": "Corporate",
            "owner_operator": "Charlie Brown",
            "registration_status": "Maintenance"
        },
        {
            "vin": "VIN_TOYOTA_XYZ789",
            "manufacturer": "Toyota",
            "model": "bZ4X",
            "fleet_id": "Personal",
            "owner_operator": "Diana Prince",
            "registration_status": "Active"
        }
    ]

    print("--- Starting Database Seeding ---")
    
    for vehicle_data in vehicles_to_create:
        try:
            response = requests.post(endpoint, json=vehicle_data)
            
            if response.status_code == 201:
                print(f"Successfully created vehicle with VIN: {vehicle_data['vin']}")
            else:
                print(f"Failed to create vehicle with VIN: {vehicle_data['vin']}")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.json()}")

        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: Could not connect to the API at {BASE_URL}.")
            print("Please make sure your FastAPI server is running.")
            break 
    
    print("--- Seeding Finished ---")

if __name__ == "__main__":
    seed_data()