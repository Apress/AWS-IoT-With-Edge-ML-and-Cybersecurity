import paho.mqtt.client as mqtt
import time
import random
import ssl

# Configuration
BROKER_HOST = "localhost"
BROKER_PORT = 8883
TOPIC = "devices/thermostat/data/value"
CLIENT_ID = "Thermostat"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed with code {rc}")

# Set up the MQTT client
client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.tls_set(ca_certs="ca.pem", certfile="Thermostat.crt", keyfile="Thermostat.key")

# Connect to the broker
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_start()  # Start the loop to handle background tasks

def simulate_thermostat():
    time.sleep(2)  # Give some time for the connection to establish

    for _ in range(3):  # Simulate 3 times
        # Generate random temperature data
        temperature = round(20 + (random.random() * 5), 2)
        humidity = round(40 + (random.random() * 20), 2)
        aqi = round(random.random() * 300)

        # Construct the payload
        payload = f"Temperature: {temperature}°C, Humidity: {humidity}%, AQI: {aqi}"

        # Publish the payload
        result = client.publish(TOPIC, payload, qos=0)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Published: {payload}")
        else:
            print(f"Failed to publish. Reason code: {result.rc}")
        
        time.sleep(3)  # Pause between simulations

if __name__ == "__main__":
    try:
        simulate_thermostat()
        time.sleep(4)  # Give some time for the last publish operation to complete
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
