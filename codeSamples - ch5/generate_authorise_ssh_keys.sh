#!/bin/bash

DEFAULT_PATH=~/.ssh/id_rsa  # No quotes around the path and point it directly to the key file

# Check if the key already exists
if [ -e "$DEFAULT_PATH" ]; then
    echo "Error: Key file already exists at $DEFAULT_PATH"
    exit 2
fi

# Check SSH folder if it doesn't exist
if [ ! -d ~/.ssh ]; then
    mkdir ~/.ssh
    chmod 700 ~/.ssh
fi

# Generate the key without a passphrase
ssh-keygen -t rsa -b 4096 -m PEM -f "$DEFAULT_PATH" -N ""

echo "SSH key generated at $DEFAULT_PATH"

# Append the generated public key to authorized_keys
cat "${DEFAULT_PATH}.pub" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo "Public key added to ~/.ssh/authorized_keys"

# Notify the user about the private key
echo "Please securely copy the 'private key' from: $DEFAULT_PATH"
