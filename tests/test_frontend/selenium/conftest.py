import json
import logging

import pytest
import requests
from selene import browser
from selene.support.shared import config
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection

# from config import (
#     NAME_PRODUCT,
#     REMOTE_BROWSER_NAME,
#     REMOTE_BROWSER_SESSIONS,
#     REMOTE_BROWSER_VERSION,
#     REQUESTS_CA_BUNDLE,
#     SUNKEY_API,
#     SUNKEY_AUTHORIZATION,
#     SUNKEY_SOL_CODE,
#     TESTING_TYPE_REALISE,
# )
from pages.main_page import MainPage


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
        # options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)
    # elif mode_browser == 'remote':
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': SUNKEY_AUTHORIZATION
    #     }
    #     data = {
    #         'productSolCode': SUNKEY_SOL_CODE,
    #         'name': NAME_PRODUCT,
    #         'testingType': TESTING_TYPE_REALISE,
    #         'browsers': [
    #             {
    #                 'name': REMOTE_BROWSER_NAME,
    #                 'sessions': REMOTE_BROWSER_SESSIONS,
    #                 'version': REMOTE_BROWSER_VERSION
    #             }
    #         ]
    #     }
    #     response = requests.post(SUNKEY_API, headers=headers, json=data, timeout=300, verify=REQUESTS_CA_BUNDLE)
    #     response_data = json.loads(response.text)
    #     connection_string = response_data['connectionString']
    #     print(connection_string)
    #     RemoteConnection.set_certificate_bundle_path(None)
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--ignore-certificate-errors')
    #     options.set_capability("selenoid:options", {
    #         "enableVideo": False,
    #         "enableVNC": False,
    #         "acceptInsecureCerts": True,
    #         "networkConnectionEnabled": True
    #     })
    #     driver = webdriver.Remote(
    #         command_executor=connection_string,
    #         options=options
    #     )
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
    main_page.check_oracle_logo()
