# Cycognito - Task

Web scraping tool that extracts data from a list of URLs.
The tool uses the Selenium WebDriver to scrape the data and save it in a JSON file.
The tool also takes a screenshot of the URL and saves it as a PNG file.

# Installation
```bash
git clone https://github.com/ronnuriel/Cycognito.git
cd Cycognito
```

Run Docker container linux or mac
```bash
./run.sh
```
Run Docker container windows
```bash
./run.ps1
```

if you have permission issues, run the following command
```bash
chmod +x run.sh
```

Run the application without Docker
```bash
python browser_module.py
```

# Overview
## Project Structure
```
.
├── Dockerfile                 # Dockerfile for containerizing the application.
├── README.md                  # This README file.
├── browser_module.py          # Main Python script for web scraping.
├── input                      # Directory containing input files.
│   └── urls.input             # Text file with URLs to scrape.
├── output                     # Output directory for scraped data.
│   └── url_X                  # Each subdirectory contains results for a URL.
│       ├── browse.json        # JSON file with scraped data.
│       └── screenshot.png     # Screenshot of the URL.
├── requirements.txt           # Python dependencies.
├── run.sh                     # Shell script to run the application.
└── testMain.py                # Unit tests for the application.
'
```

clean output directory
```bash
rm -rf output/*
```


## **Run Tests**
```bash
python -m pytest testMain.py
```
