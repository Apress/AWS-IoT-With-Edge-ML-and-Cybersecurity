#FileName: shadowUpdate.py

import json
import asyncio
import time
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted. error: {error}")

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")

# Callback when the subscribed message is received. 
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload}")
    print("--------------")

async def get_and_update_shadow():
    #### Replace start
    endpoint = "your-iot-endpoint.amazonaws.com"      #Replace with your AWS IoT Core endpoint
    cert_filepath = "path/to/certificate.pem.crt"       #Replace with the path to your device certificate
    pri_key_filepath = "path/to/private/private-key.pem.key"     #Replace with the path to your private key
    ca_filepath = "path/to/root/ca.pem"     #Replace with the path to your root CA certificate
    client_id = "shadowUpdateThing"          #Replace if different
    thing_name = "shadowUpdateThing"         #Replace if different
    shadow_name = "testShadow"               #Replace if different 
    ####Replace End

    # Initiate MQTT connection
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=cert_filepath,
        pri_key_filepath=pri_key_filepath,
        client_bootstrap=client_bootstrap,
        ca_filepath=ca_filepath,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=6
    )

    print(f"Connecting to {endpoint} with client ID '{client_id}'...")
    connect_future = mqtt_connection.connect()
    while not connect_future.done():
        time.sleep(0.1)
    print("Connected!")

    # First, let's get the current shadow state.
    print(f"Subscribing to topic $aws/things/{thing_name}/shadow/name/{shadow_name}/get/accepted...")
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=f"$aws/things/{thing_name}/shadow/name/{shadow_name}/get/accepted",
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )
    
    while not subscribe_future.done():
        time.sleep(0.1)
    print("Subscribed.")

    # Now that we're subscribed, let's send a get request.
    print(f"Publishing get request to $aws/things/{thing_name}/shadow/name/{shadow_name}/get...")
    mqtt_connection.publish(
        topic=f"$aws/things/{thing_name}/shadow/name/{shadow_name}/get",
        payload=json.dumps({}),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    # Wait for a few seconds to receive the response
    await asyncio.sleep(3)

    # Now let's update the shadow
    message = {
        "state": {
            "desired": {
                "temperature": 22     #Replace this for your testing
            }
        }
    }
    print(f"Publishing update to $aws/things/{thing_name}/shadow/name/{shadow_name}/update...")
    mqtt_connection.publish(
        topic=f"$aws/things/{thing_name}/shadow/name/{shadow_name}/update",
        payload=json.dumps(message),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    while not disconnect_future.done():
        time.sleep(0.1)
    print("Disconnected")

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(get_and_update_shadow())

