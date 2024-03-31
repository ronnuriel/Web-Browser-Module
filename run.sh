#!/bin/bash

# build the docker image
docker build -t hometask/browser_module .
docker run -v /Users/ronnuriel/git/Cycognito/input:/input -v /Users/ronnuriel/git/Cycognito/output:/output -it hometask/browser_module
