#fileName: myFirstIoTDeviceVirtual.py

import random
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core configuration
#REPLACE settings details below per your settings

#### Replace start

endpoint = "your-iot-endpoint.amazonaws.com"      #Replace with your AWS IoT Core endpoint
root_ca_path = "path/to/root/ca.pem"     #Replace with the path to your root CA certificate
private_key_path = "path/to/private/key.pem"     #Replace with the path to your private key
certificate_path = "path/to/certificate.pem"       #Replace with the path to your device certificate
client_id = " myFirstIoTDevice "          #Replace if you used different thing name

# Define the topic to publish to
topic = "awsiotbook/myTopic"            #Replace with the topic you want to publish to
####Replace End


# Create an MQTT client
mqtt_client = AWSIoTMQTTClient(client_id)
mqtt_client.configureEndpoint(endpoint, 8883)
mqtt_client.configureCredentials(root_ca_path, private_key_path, certificate_path)

# Connect to AWS IoT Core
mqtt_client.connect()

for _ in range(5):
    # Create a JSON payload with random temperature value
    payload = {
        "sensor": "temperature",
        "value": random.randint(20, 30),
        "timestamp": int(time.time())
    }

    # Publish the JSON payload to the topic
    mqtt_client.publish(topic, json.dumps(payload), 1)

    # Wait for a short interval before the next iteration
    time.sleep(2)

# Disconnect from AWS IoT Core
mqtt_client.disconnect()
