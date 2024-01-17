import random
import sys
import time
import uuid

import boto3


class ConveyorBeltSimulator:
    def __init__(self):
        self.motor_temperature = random.uniform(20, 50)
        self.belt_speed = random.uniform(0.5, 2)
        self.vibration = random.uniform(0.05, 0.2)
        self.operational_hours = 0
        self.emergency_stops = 0

    def simulate_data(self):
        self.motor_temperature += random.uniform(-1, 1)
        self.belt_speed += random.uniform(-0.05, 0.05)
        self.vibration += random.uniform(-0.01, 0.01)
        self.operational_hours += 0.0167
        if random.random() < 0.20:
            self.emergency_stops += 1

    def send_data_to_cloud(self):
        data = {
            "motor_temperature": self.motor_temperature,
            "belt_speed": self.belt_speed,
            "vibration": self.vibration,
            "operational_hours": self.operational_hours,
            "emergency_stops": self.emergency_stops,
        }

        client = boto3.client("iotsitewise")
        asset_id = "REPLACE_HERE"  # OBTAIN FROM IoTSiteWise > Assets > Asset ID

        # Creating batch entries for each property value
        entries = []

        #  OBTAIN FROM IoTSiteWise > Assets > Measurements > ID for each metric.
        property_mapping = {
            "motor_temperature": "REPLACE_HERE",
            "belt_speed": "REPLACE_HERE",
            "vibration": "REPLACE_HERE",
            "operational_hours": "REPLACE_HERE",
            "emergency_stops": "REPLACE_HERE",
        }

        for prop, value in data.items():
            entries.append(
                {
                    "entryId": str(uuid.uuid4()),
                    "assetId": asset_id,
                    "propertyId": property_mapping[prop],
                    "propertyValues": [
                        {
                            "value": {"doubleValue": value},
                            "timestamp": {"timeInSeconds": int(time.time())},
                        }
                    ],
                }
            )

        try:
            client.batch_put_asset_property_value(entries=entries)
        except boto3.exceptions.Boto3Error as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    def run_simulation(self, duration_minutes):
        for _ in range(duration_minutes):
            self.simulate_data()
            self.send_data_to_cloud()
            time.sleep(60)


if __name__ == "__main__":
    simulator = ConveyorBeltSimulator()
    simulator.run_simulation(10)
