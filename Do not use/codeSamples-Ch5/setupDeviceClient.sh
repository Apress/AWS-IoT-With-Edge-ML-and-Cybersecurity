#!/bin/bash

# Detecting the package manager
if command -v yum &> /dev/null; then
    PACKAGE_MANAGER="yum"
    EXTRA_INSTALL="sudo amazon-linux-extras install epel -y && sudo yum groupinstall 'Development Tools' -y"
elif command -v apt-get &> /dev/null; then
    PACKAGE_MANAGER="apt-get"
    EXTRA_INSTALL="sudo apt-get install -y build-essential"
else
    echo "Neither yum nor apt-get found. Exiting."
    exit 1
fi

# If it's Amazon Linux, add EPEL and install Development Tools
if [ "$PACKAGE_MANAGER" = "yum" ]; then
    eval $EXTRA_INSTALL
fi

# Variables
OPENSSL_VERSION=1.1.1n

# Update and install necessary tools
sudo $PACKAGE_MANAGER update -y
sudo $PACKAGE_MANAGER install -y tar bzip2 git wget curl sudo make gcc g++
[ "$PACKAGE_MANAGER" = "yum" ] && sudo yum clean all && sudo rm -rf /var/cache/yum

# Install pre-built CMake
cd /tmp
curl -sSL https://github.com/Kitware/CMake/releases/download/v3.10.0/cmake-3.10.0.tar.gz -o cmake-3.10.0.tar.gz
tar -zxvf cmake-3.10.0.tar.gz
cd cmake-3.10.0
./bootstrap
make
sudo make install

# Install OpenSSL 1.1.1
cd /tmp
wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz
tar -zxvf openssl-${OPENSSL_VERSION}.tar.gz
cd openssl-${OPENSSL_VERSION}
./config
make
sudo make install

# Install AWS IoT Device Client
cd ~
git clone https://github.com/awslabs/aws-iot-device-client.git
mkdir ~/device-client
chmod 745 ~/device-client
touch ~/device-client/subscribe-file.txt
chmod 600 ~/device-client/subscribe-file.txt
cd aws-iot-device-client
mkdir build
cd build
cmake ../
cmake --build . --target aws-iot-device-client
