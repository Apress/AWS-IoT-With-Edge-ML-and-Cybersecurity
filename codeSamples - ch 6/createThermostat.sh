#!/bin/bash

# Install paho using pip
pip3 install paho-mqtt

# Create 'devices' directory if it doesn't exist and then create thing file
mkdir -p ~/environment/devices/thermostat
cd ~/environment/devices/thermostat
touch thermostatThing.py

# Define the name of the IoT thing
THING_NAME=Thermostat

# Create the IoT thing on AWS
aws iot create-thing --thing-name $THING_NAME

# Create keys and certificate for the IoT thing and store the ARN in CERTIFICATE_ARN
CERTIFICATE_ARN=$(aws iot create-keys-and-certificate --private-key-out $THING_NAME.key --certificate-pem-out $THING_NAME.crt --query "certificateArn" --out text --set-as-active)

# Attach the created thing to the certificate
aws iot attach-thing-principal --thing-name $THING_NAME --principal $CERTIFICATE_ARN

# Attach the policy named 'myFirstPolicy' to the certificate
aws iot attach-policy --policy-name myFirstPolicy --target $CERTIFICATE_ARN

cd ~/environment/devices/thermostat
sudo cp /greengrass/v2/work/aws.greengrass.clientdevices.Auth/ca.pem .
sudo chmod 444 ca.pem 

# Output a success message
echo "Device Thermostat created, and policy setup completed successfully!"
