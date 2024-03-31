#FROM ubuntu:latest
#LABEL authors="ronnuriel"
#
#ENTRYPOINT ["top", "-b"]
# Use an official Python runtime as a parent image
FROM python:3.8-slim
LABEL authors="ronnuriel"

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file, to cache the installed dependencies
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Copy the rest of your application's source code from your host to your image filesystem.
COPY . /app

## Make port 80 available to the world outside this container
#EXPOSE 80

## Define environment variable
#ENV NAME World

# Run browser_module.py when the container launches
CMD ["python", "./browser_module.py"]
