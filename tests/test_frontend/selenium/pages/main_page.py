from pages.base_page import BasePage
from selene import be, browser
from locators.main_page_locators import MainPageLocators
from config import TABS_URL


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
