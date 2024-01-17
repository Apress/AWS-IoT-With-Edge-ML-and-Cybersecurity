import json
import random
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core endpoint
iot_endpoint = "REPLACE_HERE"  # Replace with your AWS IoT Endpoint URL, use command: aws iot describe-endpoint --endpoint-type iot:Data-ATS

# AWS IoT Thing Name
thing_name = "impersonationAttackThing"

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


def generate_metrics_data():
    return {
        "AuthorizationFailures": random.choice(
            [0, 1, 2]
        ),  # Most of the time it's 0, but occasionally 1 or 2 to simulate an anomaly
        "ConnectionAttempts": random.choice([1, 2]),  # Regular connection attempts
        "Disconnects": random.choice([0, 1]),  # Occasionally disconnects
        "ClientIDVerifier": str(
            random.randint(1000, 9999)
        ),  # Assuming this is a random value for each device's session
        "SourceIP": f"192.168.{random.randint(0,255)}.{random.randint(0,255)}",  # Simulating random source IP
    }


# Infinite loop to publish metrics data
while True:
    metrics_data = generate_metrics_data()
    mqtt_client.publish(
        "/awsiotbook/deviceDefender/impersonationMetrics", json.dumps(metrics_data), 1
    )
    print(f"Published: {json.dumps(metrics_data)}")
    time.sleep(10)  # Wait for 10 seconds before publishing the next set of metrics
