import pytest
from browser_module import get_network_resources  # Adjust this import based on your actual script name and location


@pytest.fixture
def mock_driver(monkeypatch):
    class MockDriver:
        def get_log(self, log_type):
            assert log_type == "performance"
            # Return a sample log entry that includes 'type' in 'params'
            return [
                {
                    "message": '{"message": {"method": "Network.responseReceived", "params": {"type": "Document", "requestId": "12345", "response": {"url": "https://example.com", "status": 200}}}}'
                },
                {
                    "message": '{"message": {"method": "Network.responseReceived", "params": {"type": "Stylesheet", "requestId": "67890", "response": {"url": "https://anotherexample.com", "status": 404}}}}'
                },
                # Include a log entry without 'type' in 'params'
                {
                    "message": '{"message": {"method": "Network.responseReceived", "params": {"requestId": "111213", "response": {"url": "https://missingtype.com", "status": 500}}}}'
                },
                # Include a log entry without 'response' to test the KeyError handling
                {
                    "message": '{"message": {"method": "Network.responseReceived", "params": {"type": "Image", "requestId": "141516"}}}'
                }
            ]

    monkeypatch.setattr("selenium.webdriver.Chrome", MockDriver)
    return MockDriver()


def test_get_network_resources_valid_data(mock_driver):
    resources = get_network_resources(mock_driver)

    # Check if all URLs are valid, status codes are within acceptable HTTP range, and entries meet the condition
    for resource in resources:
        assert resource["url"].startswith("https://"), f"URL {resource['url']} is not valid."
        assert 100 <= resource["status"] < 600, f"Status code {resource['status']} is out of range."

    # Ensure that the function correctly processed only entries with 'type' in 'params' and 'response' details
    assert len(resources) == 2, f"Expected 2 resources, got {len(resources)}"
