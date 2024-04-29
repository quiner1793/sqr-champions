from locators.thread_page_locators import ThreadPageLocators
from pages.base_page import BasePage


class ThreadPage(BasePage):
    @staticmethod
    def enter_feedback(feedback: str):
        ThreadPageLocators.feedback.send_keys(feedback)

    @staticmethod
    def submit():
        ThreadPageLocators.submit.click()
