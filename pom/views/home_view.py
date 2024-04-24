import pytest
from selenium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from views.base_view import BaseView


class HomeView(BaseView):
    USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, 'test-Username')
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, 'test-Password')
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN')
    SHOPPING_CART = (AppiumBy.XPATH, '//XCUIElementTypeOther[@name="test-Cart"]')

    def sign_in(self):
        self.wait_for(self.USERNAME_FIELD).send_keys('standard_user')
        self.wait_for(self.PASSWORD_FIELD).send_keys('secret_sauce')
        self.wait_for(self.LOGIN_BUTTON).click()
        self.wait_for(self.SHOPPING_CART)
        status = "passed" if self.SHOPPING_CART else "failed"
        self.driver.execute_script("sauce:job-result={}".format(status))


