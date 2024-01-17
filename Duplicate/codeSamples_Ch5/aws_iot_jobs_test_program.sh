#!/bin/bash

# Define the output file path
OUTPUT_FILE="/var/log/AWSIoTJobs-test-program-output.txt"

# Check if the user has permission to write to the file or create a new one in /var/log/
if [ ! -w "$OUTPUT_FILE" ] && [ ! -w "/var/log/" ]; then
    echo "Permission denied to write to $OUTPUT_FILE. Try running the script with sudo."
    exit 1
fi

# Write a message to the output file
echo "Test data from the AWS IoT Jobs test program: $(date)" >> $OUTPUT_FILE

echo "Data written to $OUTPUT_FILE"
