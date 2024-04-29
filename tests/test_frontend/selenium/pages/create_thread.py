from pages.base_page import BasePage
from locators.create_thread_locators import CreateThreadLocators


class CreateThreadPage(BasePage):
    @staticmethod
    def enter_url(url: str):
        CreateThreadLocators.url.send_keys(url)

    @staticmethod
    def enter_comment(comment: str):
        CreateThreadLocators.feedback.send_keys(comment)

    @staticmethod
    def create_thread():
        CreateThreadLocators.create_btn.click()
