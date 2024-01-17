# This code simulates metrics anomalies which can be used to test AWS IoT Device Defender's rules profile for potential ransomware activities.
# Adjust the ranges or values for your testing.


import json
import random
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core endpoint
iot_endpoint = "REPLACE_HERE"  # Replace with your AWS IoT Endpoint URL, use command: aws iot describe-endpoint --endpoint-type iot:Data-ATS

# AWS IoT Thing Name
thing_name = "simulateRansomThing"

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


def generate_ransomware_metrics():
    tcp_ports = random.sample(
        range(1024, 65535), random.randint(5, 20)
    )  # Ports above 1024 to simulate dynamically assigned ports
    udp_ports = random.sample(range(1024, 65535), random.randint(5, 20))
    return {
        "DestinationIP": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",  # Potentially suspicious destination IP
        "ListeningTCPPorts": tcp_ports,
        "ListeningTCPPortCount": len(tcp_ports),
        "ListeningUDPPorts": udp_ports,
        "ListeningUDPPortCount": len(udp_ports),
    }


# Infinite loop to publish ransomware metrics
while True:
    ransomware_metrics = generate_ransomware_metrics()
    mqtt_client.publish(
        "/awsiotbook/deviceDefender/ransomwareMetrics",
        json.dumps(ransomware_metrics),
        1,
    )
    print(f"Published: {json.dumps(ransomware_metrics)}")
    time.sleep(10)  # Wait for 10 seconds before publishing the next set of metrics
