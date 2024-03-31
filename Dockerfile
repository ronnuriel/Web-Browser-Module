FROM joyzoursky/python-chromedriver:latest

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file, to cache the installed dependencies
COPY requirements.txt /app/


# Install the dependencies
RUN pip install -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run browser_module.py when the container launches
CMD ["python", "./browser_module.py"]