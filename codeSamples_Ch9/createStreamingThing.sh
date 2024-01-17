#!/bin/bash

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
    echo "The jq tool is not installed. Please install it and rerun the script."
    exit 1
fi

# Check if the /home/ubuntu/environment/ directory exists
if [ -d "/home/ubuntu/environment/" ]; then
    BASE_DIR="/home/ubuntu/environment"
else
    BASE_DIR="$HOME"
fi

# Create a directory named "bus" if it doesn't exist
EV_DIR="$BASE_DIR/bus"
mkdir -p "$EV_DIR"

THING_NAME="PublicTransportBus"
THING_SUBDIR="$EV_DIR/$THING_NAME"

# Create a new thing
aws iot create-thing --thing-name "$THING_NAME"
if [ $? -ne 0 ]; then
    echo "Failed to create thing using AWS CLI"
    exit 1
fi

# Create a certificate for the thing
aws iot create-keys-and-certificate --set-as-active > "$THING_NAME-certificate-output.json"
if [ $? -ne 0 ]; then
    echo "Failed to create keys and certificate using AWS CLI"
    exit 1
fi

# Extract certificate ARN
CERT_ARN=$(jq -r .certificateArn "$THING_NAME-certificate-output.json")
if [ $? -ne 0 ]; then
    echo "Failed to parse certificate ARN using jq"
    exit 1
fi

# Attach the certificate to the thing
aws iot attach-thing-principal --thing-name "$THING_NAME" --principal "$CERT_ARN"
if [ $? -ne 0 ]; then
    echo "Failed to attach thing principal using AWS CLI"
    exit 1
fi

# Check if "myFirstDemoNonProductionPolicy" exists
if ! aws iot get-policy --policy-name myFirstDemoNonProductionPolicy &> /dev/null; then
    # If not, create myFirstDemoNonProductionPolicy
    # DO NOT use in production this policy as its for education and for learning purpose ONLY!
    aws iot create-policy --policy-name myFirstDemoNonProductionPolicy --policy-document '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "iot:*",
          "Resource": "*"
        }
      ]
    }'
    if [ $? -ne 0 ]; then
        echo "Failed to create policy using AWS CLI"
        exit 1
    fi
fi

CERT_ID=$(jq -r .certificateId "$THING_NAME-certificate-output.json")
if [ $? -ne 0 ]; then
    echo "Failed to parse certificate ID using jq"
    exit 1
fi

aws iot attach-policy --policy-name myFirstDemoNonProductionPolicy --target "$CERT_ARN"
if [ $? -ne 0 ]; then
    echo "Failed to attach policy using AWS CLI"
    exit 1
fi

# Create a subdirectory for the thing and store certificate, private key, and Amazon root CA in it
mkdir -p "$THING_SUBDIR"
jq -r .certificatePem "$THING_NAME-certificate-output.json" > "$THING_SUBDIR/certificate.pem.crt"
if [ $? -ne 0 ]; then
    echo "Failed to write certificate PEM using jq"
    exit 1
fi

jq -r .keyPair.PrivateKey "$THING_NAME-certificate-output.json" > "$THING_SUBDIR/private.pem.key"
if [ $? -ne 0 ]; then
    echo "Failed to write private key using jq"
    exit 1
fi

curl -o "$THING_SUBDIR/AmazonRootCA1.pem" https://www.amazontrust.com/repository/AmazonRootCA1.pem
if [ $? -ne 0 ]; then
    echo "Failed to download Amazon root CA"
    exit 1
fi

echo "Certificate, private key, and Amazon root CA for $THING_NAME downloaded to $THING_SUBDIR."
