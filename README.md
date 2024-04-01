# Cycognito

```bash
git clone https://github.com/ronnuriel/Cycognito.git
cd Cycognito
```

Run Docker container
```bash
./run.sh
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
├── __pycache__                # Compiled Python files (automatically generated).
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