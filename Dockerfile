#FROM ubuntu:latest
#LABEL authors="ronnuriel"
#
#ENTRYPOINT ["top", "-b"]
# Use an official Python runtime as a parent image
FROM python:3.8-slim
LABEL authors="ronnuriel"

# Set environment variables to make Chrome run in a headless environment
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies required for adding Google Chrome repository and other utilities
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Add the Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install dependencies for downloading and installing Chrome
RUN apt-get update && apt-get install -y wget dpkg --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Clean up
RUN rm google-chrome-stable_current_amd64.deb

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME World

# Run browser_module.py when the container launches
CMD ["python", "./browser_module.py"]
