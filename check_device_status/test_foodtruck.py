import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Sauce Labs Appium remote URL (credentials will be added dynamically)
APPIUM_SERVER_BASE_URL = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"


@pytest.fixture(scope="class")
def driver(request):
    """
    Initialize Appium driver for iOS device testing on Sauce Labs.
    
    Capabilities can be customized via environment variables:
    - DEVICE_ID: Specific device to run on (from SELECTED_DEVICE_ID env var)
    - APP_PATH: Path to the app bundle or app ID
    """
    
    # Get Sauce Labs credentials from environment
    username = os.environ.get("SAUCE_USERNAME")
    access_key = os.environ.get("SAUCE_ACCESS_KEY")
    
    if not username or not access_key:
        raise ValueError("SAUCE_USERNAME and SAUCE_ACCESS_KEY environment variables are required")
    
    # Create Appium options for iOS (use W3C-style capabilities and Appium 2)
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'

    # Vendor-prefixed (W3C) Appium capabilities
    options.set_capability('appium:deviceName', 'iPhone_SE_2020_POC132||iPhone_SE_2020_POC124')
    options.set_capability('appium:app', 'storage:filename=FoodTruck.ipa')

    # Sauce Labs (sauce:options) - request Appium 2.x explicitly
    sauce_options = {
        'username': username,
        'accessKey': access_key,
        'appiumVersion': 'latest',
        'build': 'Python Service - Check Device Status - Run 2',
        'name': 'Food Truck Test'
    }
    options.set_capability('sauce:options', sauce_options)

    # Build the remote URL with credentials for authentication
    remote_url = f"https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub"

    # Initialize the Appium driver
    appium_driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )
    
    yield appium_driver
    
    # Cleanup
    appium_driver.quit()


# ===== Alerts Feature Tests =====
# Converted from WebdriverIO JavaScript tests

class TestAlerts:
    """Test suite for Alerts feature"""
    
    def test_should_tap_on_alerts(self, driver):
        try:
            print(f"Sauce Session: https://app.saucelabs.com/tests/{driver.session_id}")
            
            # Wait for the alerts button to be displayed (5 second timeout)
            wait = WebDriverWait(driver, 5)
            orders_button = wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name=\'New Orders\']"))
            )
            
            # Click the alerts button
            orders_button.click()
            print("Successfully tapped on the orders button")

            
            # Click the order 1224 button
            generate_button = wait.until(
                EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Order#1224"))
            )
            generate_button.click()
            print("Successfully tapped on the order")
            
            
            driver.execute_script("sauce:job-result=passed")
            assert True
        
        except Exception as e:
            print(f"Failed to tap on alerts: {e}")
            driver.execute_script("sauce:job-result=failed")
            raise e