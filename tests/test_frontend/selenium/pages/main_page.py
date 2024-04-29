from config import TABS_URL
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from selene import browser


class MainPage(BasePage):
    @staticmethod
    def open_main_page():
        browser.open(TABS_URL)

    @staticmethod
    def enter_query(query: str):
        MainPageLocators.enter_query.send_keys(query)

    @staticmethod
    def search():
        MainPageLocators.search_btn.click()

    @staticmethod
    def open_create_thread():
        MainPageLocators.create_thread_btn.click()

    @staticmethod
    def open_profile():
        MainPageLocators.profile_page.click()

    @staticmethod
    def open_comment_hub():
        MainPageLocators.comment_hub_page.click()

    @staticmethod
    def open_thread_page():
        MainPageLocators.first_element_search.click()
