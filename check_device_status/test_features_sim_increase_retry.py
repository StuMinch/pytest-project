import uuid
import pytest
import os

import urllib3
from urllib3.util.retry import Retry

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Sauce Labs Appium remote URL (credentials will be added dynamically)
APPIUM_SERVER_BASE_URL = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"


def make_retrying_http_client():
    retry = Retry(
        total=30,             # up to 30 retries
        redirect=30,          # up to 30 redirect retries
        backoff_factor=1.0,   # exponential backoff
        status_forcelist=[303],
        allowed_methods={"GET"}  # only retry GET, never POST
    )

    return urllib3.PoolManager(retries=retry)


@pytest.fixture(scope="class")
def driver(request):
    """
    Initialize Appium driver for iOS device testing on Sauce Labs,
    with a custom HTTP client that increases redirect retries.
    """

    username = os.environ.get("SAUCE_USERNAME")
    access_key = os.environ.get("SAUCE_ACCESS_KEY")

    if not username or not access_key:
        raise ValueError("SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables are required")

    # Appium capabilities
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'
    options.set_capability('appium:deviceName', 'iPhone 13 Simulator')
    options.set_capability('appium:platformVersion', '17.0')
    options.set_capability('appium:newCommandTimeout', '90')
    options.set_capability('appium:app', 'storage:1d6e86c6-5f98-47d3-a100-91a84632f40e')

    sauce_options = {
        'username': username,
        'accessKey': access_key,
        'appiumVersion': '2.11.3',
        'uuid': str(uuid.uuid4()),
        'build': 'User Abandoned Test - Custom HTTP Client',
        'name': 'Features Test'
    }
    options.set_capability('sauce:options', sauce_options)

    # Build remote URL
    remote_url = f"https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub"

    # Custom retrying HTTP client
    http_client = make_retrying_http_client()

    # Create RemoteConnection and inject custom client
    remote_conn = RemoteConnection(remote_url, keep_alive=True)
    remote_conn._conn = http_client

    # Initialize driver using the custom RemoteConnection
    appium_driver = webdriver.Remote(
        command_executor=remote_conn,
        options=options
    )

    yield appium_driver
    appium_driver.quit()


# ===== Alerts Feature Tests =====

class TestAlerts:
    """Test suite for Alerts feature"""

    def test_should_tap_on_alerts(self, driver):
        try:
            print(f"Sauce Session: https://app.saucelabs.com/tests/{driver.session_id}")

            wait = WebDriverWait(driver, 5)

            alerts_button = wait.until(
                EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Alerts"))
            )
            alerts_button.click()
            print("Successfully tapped on alerts button")

            generate_button = wait.until(
                EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Generate Alert"))
            )
            generate_button.click()
            print("Successfully tapped on generate alert button")

            ok_button = wait.until(
                EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "OK"))
            )
            ok_button.click()
            print("Successfully tapped on OK button")

            driver.execute_script("sauce:job-result=passed")
            assert True

        except Exception as e:
            print(f"Failed to tap on alerts: {e}")
            driver.execute_script("sauce:job-result=failed")
            raise e
