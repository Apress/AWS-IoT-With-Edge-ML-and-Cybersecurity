import json
import random
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core endpoint
iot_endpoint = "REPLACE_HERE"  # Replace with your AWS IoT Endpoint URL

# AWS IoT Thing Name
thing_name = "simulateCryptoJackingThing"

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


def generate_cryptojacking_metrics():
    return {
        "Destination_IPs": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",  # Always outside of CIDR 192.168.101.0/24
        "CPU": random.uniform(80, 100),  # Always greater than or equal to 80
        "Memory": random.uniform(75, 100),  # Always greater than or equal to 75
        "ChipTemperature": random.randint(
            100, 120
        ),  # Always greater than or equal to 100
        "Voltage": random.uniform(3.1, 3.3),  # Always greater than 3
        "SourceIP": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",  # Outside of CIDR 192.168.99.0/24
    }


# Infinite loop to publish cryptojacking metrics
while True:
    cryptojacking_metrics = generate_cryptojacking_metrics()
    mqtt_client.publish(
        "/awsiotbook/deviceDefender/cryptojackingMetrics",
        json.dumps(cryptojacking_metrics),
        1,
    )
    print(f"Published: {json.dumps(cryptojacking_metrics)}")
    time.sleep(10)  # Wait for 5 minutes before publishing the next set of metrics
