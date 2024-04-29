from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """def __init__(self, browser: webdriver, url, timeout=5):
        self.browser = browser
        self.url = url
        self.browser.implicity_wait(timeout)

    def open(self):
        self.browser.get(self.url)"""

    def is_element_present(self, how, locator):
        try:
            self.browser.find_element(how, locator)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, locator, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(
                ec.presence_of_element_located((how, locator))
            )
        except TimeoutException:
            return True

        return False

    def is_disappeared(self, how, locator, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, [TimeoutException]).until_not( # noqa
                ec.presence_of_element_located((how, locator))
            )
        except TimeoutException:
            return False
        return True
