import pytest
from selenium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from views.base_view import BaseView


class HomeView(BaseView):
    USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, 'test-Username')
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, 'test-Password')
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'test-LOGIN')
    ANDROID_SHOPPING_CART = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Cart"]')
    IOS_SHOPPING_CART = (AppiumBy.XPATH, '//XCUIElementTypeOther[@name="test-Cart"]')

    def sign_in(self):
        self.wait_for(self.USERNAME_FIELD).send_keys('standard_user')
        self.wait_for(self.PASSWORD_FIELD).send_keys('secret_sauce')
        self.wait_for(self.LOGIN_BUTTON).click()
        if BaseView.platformName == 'iOS':
            shopping_cart = self.wait_for(self.IOS_SHOPPING_CART)
        elif BaseView.platformName == 'Android':
            shopping_cart = self.wait_for(self.ANDROID_SHOPPING_CART)
        else:
            raise Exception(f"Unsupported platform: {platform}")
        status = "passed" if shopping_cart else "failed"
        self.driver.execute_script("sauce:job-result={}".format(status))
