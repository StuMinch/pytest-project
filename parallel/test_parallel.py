import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import os

remote_url = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"


@pytest.fixture(scope="class")
def driver(request):
    options = Options()
    options.browser_version = 'latest'
    options.platform_name = 'Windows 10'

    sauce_options = {}
    sauce_options['username'] = os.environ.get("SAUCE_USERNAME")
    sauce_options['accessKey'] = os.environ.get("SAUCE_ACCESS_KEY")
    sauce_options['build'] = 'Pytest Parallel Test'
    sauce_options['name'] = 'Check Page Title'
    options.set_capability('sauce:options', sauce_options)

    driver = webdriver.Remote(command_executor=remote_url, options=options)
    yield driver
    driver.quit()


@pytest.mark.parametrize(
    "url, expected_title",
    [
        ("https://sony.com", "Sony Group Portal - Home"),
        ("https://saucelabs.com", "Sauce Labs: Cross Browser Testing, Selenium Testing & Mobile Testing"),
    ],
)
def test_page_title(driver, url, expected_title):
    print(f"Sauce Session: https://app.saucelabs.com/tests/{driver.session_id}")
    driver.get(url)
    status = "passed" if driver.title == expected_title else "failed"
    driver.execute_script("sauce:job-result={}".format(status))
    assert driver.title == expected_title, f"Page title mismatch. Expected: {expected_title}, Actual: {driver.title}"
