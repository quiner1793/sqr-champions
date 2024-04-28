from pages.base_page import BasePage
from locators.sign_up_locators import SignUpLocators


class SignUpPage(BasePage):
    @staticmethod
    def enter_username(username: str):
        SignUpLocators.username.send_keys(username)

    @staticmethod
    def enter_email(email: str):
        SignUpLocators.email.send_keys(email)

    @staticmethod
    def enter_password(password: str):
        SignUpLocators.password.send_keys(password)

    @staticmethod
    def create_account():
        SignUpLocators.create_account.click()
