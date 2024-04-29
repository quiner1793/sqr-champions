
import logging

import pytest
from pages.main_page import MainPage
from selene import browser
from selene.support.shared import config
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--browser", help="Test browser", choices=["chrome"], default="chrome"
    )
    parser.addoption(
        "--mode",
        help="Choose where exec tests",
        choices=["local", "remote"],
        default="local",
    )


def custom_driver(mode_browser):
    logging.debug("custom driver config start")
    if mode_browser == "local":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
    else:
        raise ValueError("mode_browser does not set")
    driver.set_window_size(1200, 800)
    driver.delete_all_cookies()
    config.timeout = 10
    browser.config.browser_name = driver
    browser.config.save_screenshot_on_failure = True
    browser.config.save_page_source_on_failure = False
    logging.debug("custom driver config finish")
    return driver


@pytest.fixture(scope="session")
def mode_browser(request):
    return request.config.getoption("--mode")


@pytest.fixture(scope="class")
def browser_session(mode_browser):
    config.driver = custom_driver(mode_browser)
    yield config.driver
    config.driver.quit()


@pytest.fixture(scope="function")
def browser_function(mode_browser):
    config.driver = custom_driver(mode_browser)
    yield config.driver
    config.driver.quit()


@pytest.fixture(scope="session")
def main_page():
    return MainPage()


@pytest.fixture(scope="function")
def open_main_page_function(browser_function, main_page):
    main_page.open_main_page()
