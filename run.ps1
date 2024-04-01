# Assuming this script is run from the Cycognito directory

# Set input and output directories relative to the current script location
$inputDir = "$(Get-Location)\input"
$outputDir = "$(Get-Location)\output"

# Build the Docker image
docker build -t hometask/browser_module .

# Run the Docker container, mounting the input and output directories
docker run -v "${inputDir}:/input" -v "${outputDir}:/output" -it hometask/browser_module
