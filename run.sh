#!/bin/bash

# Assuming this script is run from the Cycognito directory

# Set input and output directories relative to the current script location
input_dir="$(pwd)/input"
output_dir="$(pwd)/output"

# Build the Docker image
docker build -t hometask/browser_module .

# Run the Docker container, mounting the input and output directories
docker run -v "$input_dir:/input" -v "$output_dir:/output" -it hometask/browser_module
