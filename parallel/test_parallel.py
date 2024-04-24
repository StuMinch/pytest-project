import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import os

remote_url = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"


@pytest.fixture(scope="class")
def driver(request):
    browser = request.param
    options = getattr(Options, browser)()  # Get options based on browser type
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'

    sauce_options = {}
    sauce_options['username'] = os.environ.get("SAUCE_USERNAME")
    sauce_options['accessKey'] = os.environ.get("SAUCE_ACCESS_KEY")
    sauce_options['build'] = 'Pytest Parallel Test'
    options.set_capability('sauce:options', sauce_options)

    driver = webdriver.Remote(command_executor=remote_url, options=options)
    yield driver
    driver.quit()


def test_desktop_version(driver):
    driver.get("https://www.sony.com/")
    print(f"Browser version: {driver.capabilities['browserVersion']}")
    expected_title = 'Sony Group Portal - Home'
    assert driver.title == expected_title, f"Unexpected title: {driver.title}"


@pytest.mark.parametrize("driver", ["chrome", "edge"], indirect=True)
def test_with_different_browsers(driver):
    # Run the test with the provided browser through the fixture
    pass
