# This code simulates metrics anomalies which can be used to test AWS IoT Device Defender's rules profile for potential unauthorized access or data exfiltration attempts.
# Adjust the ranges or values based on the specific nature and context of the IoT device in question.


import json
import random
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core endpoint
iot_endpoint = "REPLACE_HERE"  # Replace with your AWS IoT Endpoint URL, use command: aws iot describe-endpoint --endpoint-type iot:Data-ATS

# AWS IoT Thing Name
thing_name = "simulateIPThing"

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


def generate_ip_protection_metrics():
    # Simulating potential unauthorized access or data exfiltration attempts
    return {
        "SourceIP": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",  # Potentially suspicious source IP
        "NumberOfMessagesReceived": random.randint(
            500, 1000
        ),  # Sudden spike in number of messages
        "MessageSize": random.randint(1000, 5000),  # Unusually large message size
    }


# Infinite loop to publish IP protection metrics
while True:
    ip_protection_metrics = generate_ip_protection_metrics()
    mqtt_client.publish(
        "/awsiotbook/deviceDefender/ipProtectionMetrics",
        json.dumps(ip_protection_metrics),
        1,
    )
    print(f"Published: {json.dumps(ip_protection_metrics)}")
    time.sleep(10)  # Wait for 10 seconds before publishing the next set of metrics
