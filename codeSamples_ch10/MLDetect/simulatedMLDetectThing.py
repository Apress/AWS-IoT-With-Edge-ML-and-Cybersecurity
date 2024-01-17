import json
import random
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core endpoint
iot_endpoint = "REPLACE_HERE"

# AWS IoT Thing Name
thing_name = "MLDetectThing"

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


def generate_anomaly_metrics():
    # Simulating values that breach the AWS IoT Device Defender metrics.
    message_content = "This is a message content crafted to breach the message size threshold. It is intentionally verbose and redundant to ensure that the content size exceeds 150 bytes. This is done to simulate a potential anomaly in the IoT Device Defender metrics."

    return {
        # Device side metrics
        "PacketsOut": random.randint(51, 100),  # Exceeds the threshold of 50
        "BytesOut": random.randint(101, 200),  # Exceeds the threshold of 100
        "DestinationIP": "10.0.0.10",  # Outside of CIDR 192.168.100.14/24
        "ListeningTCPPorts": [80, 443, 22],
        "ListeningTCPPortCount": 3,
        "ListeningUDPPorts": [53, 123],
        "ListeningUDPPortCount": 2,
        # Cloud side metrics
        "NumberOfMessagesReceived": 150,  # Exceeds the threshold of 100
        "MessageSize": len(message_content),  # Exceeds the threshold of 150 bytes
        "SourceIP": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",  # Outside of CIDR 192.168.99.0/24
        "Message": message_content,
    }


# Infinite loop to publish metrics data
while True:
    anomaly_metrics = generate_anomaly_metrics()
    mqtt_client.publish(
        "/awsiotbook/deviceDefender/MLDetectMetrics", json.dumps(anomaly_metrics), 1
    )
    print(f"Published: {json.dumps(anomaly_metrics)}")
    time.sleep(10)  # Send message every 10 seconds
