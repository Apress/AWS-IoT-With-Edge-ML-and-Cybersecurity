import json
import random
import time

import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core endpoint
iot_endpoint = "REPLACE_HERE"  # Replace with your AWS IoT Endpoint URL, use command: aws iot describe-endpoint --endpoint-type iot:Data-ATS

# AWS IoT Thing Name
thing_name = "PublicTransportBus"

# Path to the certificates and private key in the same folder as the script
cert_path = "./certificate.pem.crt"
key_path = "./private.pem.key"
root_ca_path = "./AmazonRootCA1.pem"

# Initialize AWS IoT MQTT Client
mqtt_client = AWSIoTMQTTClient(thing_name)
mqtt_client.configureEndpoint(iot_endpoint, 8883)
mqtt_client.configureCredentials(root_ca_path, key_path, cert_path)

# Connect to AWS IoT
mqtt_client.connect()

# List of buses
buses = [
    {"busNumber": "Bus101", "route": "Route A"},
    {"busNumber": "Bus102", "route": "Route B"},
    {"busNumber": "Bus103", "route": "Route C"},
    {"busNumber": "Bus104", "route": "Route D"},
    {"busNumber": "Bus105", "route": "Route E"},
]


def generate_bus_data(bus):
    return {
        "busNumber": bus["busNumber"],
        "route": bus["route"],
        "speed": random.randint(0, 60),
        "occupancyRate": random.uniform(0, 1),
        "engineTemperature": random.randint(50, 150),
        "brakeHealth": random.choice(["Good", "Moderate", "Poor"]),
    }


# Infinite loop to publish random bus data
while True:
    for bus in buses:
        bus_data = generate_bus_data(bus)
        mqtt_client.publish(
            "/awsiotbook/publicTransport/busData", json.dumps(bus_data), 1
        )
        print(f"Published: {json.dumps(bus_data)}")
        time.sleep(
            10
        )  # Wait for 10 seconds before publishing the next data for another bus
