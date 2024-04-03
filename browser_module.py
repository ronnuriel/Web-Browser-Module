import os
import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


chromedriver_path = "/usr/bin/chromedriver"

# Detect the platform/machine type
machine_type = platform.machine()

if machine_type == 'arm64':  # For M1/M2 Mac
    chromedriver_path = "/opt/homebrew/bin/chromedriver"
elif machine_type == 'x86_64':  # For Intel Mac and possibly many Linux distros
    chromedriver_path = "/usr/bin/chromedriver"


def get_network_resources(driver):
    logs = driver.get_log("performance")
    resources = []
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if log["method"] == "Network.responseReceived" and 'type' in log["params"]:
            request_id = log["params"]["requestId"]
            try:
                response_url = log["params"]["response"]["url"]
                status_code = log["params"]["response"]["status"]
                resources.append({"url": response_url, "status": status_code})
            except KeyError:
                pass  # Skip entries without response details
    return resources


def process_url(url, index, output_dir="./output"):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    caps = chrome_options.to_capabilities()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    service = Service(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    print(f"Processing URL {index}: {url}")
    driver.get(url)

    # Create directory for the URL
    url_dir = os.path.join(output_dir, f"url_{index}")
    os.makedirs(url_dir, exist_ok=True)

    # Part 1: Save HTML content
    html_content = driver.page_source

    # Part 2: Save network resources
    resources = get_network_resources(driver)

    # Part 3: Save screenshot
    screenshot_path = os.path.join(url_dir, "screenshot.png")
    driver.save_screenshot(screenshot_path)

    # Part 4: Encode screenshot in base64
    with open(screenshot_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Save output JSON
    output_data = {
        "html": html_content,
        "resources": resources,
        "screenshot": encoded_string
    }
    with open(os.path.join(url_dir, "browse.json"), "w") as json_file:
        json.dump(output_data, json_file, indent=4)

    driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Run web scraper with multiple workers.")
    parser.add_argument('--workers', type=int, default=5, help='Number of workers for parallel processing')
    parser.add_argument('--input_dir', type=str, default="./input", help='Directory containing input URLs')
    parser.add_argument('--output_dir', type=str, default="./output", help='Directory to save the output')

    args = parser.parse_args()

    with open(os.path.join(args.input_dir, "urls.input"), "r") as file:
        urls = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_url = {executor.submit(process_url, url, index + 1, args.output_dir): url for index, url in
                         enumerate(urls)}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            print(f"Processing of URL {url} is complete.")
            try:
                data = future.result()
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')

    print("All URLs processed successfully. Output files are saved in the output directory.")


if __name__ == "__main__":
    main()

