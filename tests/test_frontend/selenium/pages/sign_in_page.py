from pages.base_page import BasePage
from locators.sign_in_locators import SignInLocators


class SignInPage(BasePage):
    @staticmethod
    def open_sign_up_page():
        SignInLocators.sign_up_btn.click()

    @staticmethod
    def enter_username(username: str):
        SignInLocators.username.send_keys(username)

    @staticmethod
    def enter_password(password: str):
        SignInLocators.password.send_keys(password)

    @staticmethod
    def log_in():
        SignInLocators.log_in_btn.click()
