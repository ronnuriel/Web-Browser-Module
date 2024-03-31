import os
import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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


def main(input_dir="./input", output_dir="./output"):
    # Read URLs from input file
    with open(os.path.join(input_dir, "urls.input"), "r") as file:
        urls = file.read().splitlines()

    # Set Chrome options for headlehometaskss browsing and enable performance logging
    # options = Options()
    # options.headless = True
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument('--headless')
    # options.add_experimental_option("w3c", False)
    # options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True})
    # caps = options.to_capabilities()
    # caps["goog:loggingPrefs"] = {"performance": "ALL"}



    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.binary_location = "/usr/bin/chromium"  # Path to Chromium
    caps = chrome_options.to_capabilities()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    # Specify the direct path to chromedriver (no need to use WebDriverManager)
    service = Service(executable_path="/usr/bin/chromedriver")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)


    # Start Chrome Driver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options,
    #                           desired_capabilities=caps)

    for index, url in enumerate(urls, start=1):
        driver.get(url)

        # Create directory for the URL
        url_dir = os.path.join(output_dir, f"url_{index}")
        os.makedirs(url_dir, exist_ok=True)

        # Part 1: Save HTML content
        html_content = driver.page_source

        # Part 2: Get Web Resources
        resources = get_network_resources(driver)

        # Take screenshot for Part 3
        screenshot_path = os.path.join(url_dir, "screenshot.png")
        driver.save_screenshot(screenshot_path)

        # Encode screenshot in base64 for Part 4
        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Save output JSON
        output_data = {
            "html": html_content,
            "resources": resources,
            "screenshot": encoded_string
        }
        with open(os.path.join(url_dir, "browse.json"), "w") as json_file:
            json.dump(output_data, json_file)

    driver.quit()


if __name__ == "__main__":
    main()
