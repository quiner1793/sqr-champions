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
            WebDriverWait(self.browser, timeout, 1, [TimeoutException]).until_not(
                ec.presence_of_element_located((how, locator))
            )
        except TimeoutException:
            return False
        return True

    # @staticmethod
    # @allure.step("Очищение поля от стандартного значения {text}")
    # def clear_field_from(field_element: Element, text: str):
    #     field_element.send_keys(Keys.ARROW_RIGHT)
    #     for _ in text:
    #         field_element.send_keys(Keys.BACKSPACE)

    # @staticmethod
    # @allure.step("Вводится многострочная информация в поле")
    # def multiline(data_list: list[str], element: Element):
    #     for el in data_list:
    #         if el == data_list[-1]:
    #             element.send_keys(el, Keys.RETURN)
    #             break
    #         element.send_keys(el, Keys.ENTER)

    # @staticmethod
    # @allure.step("Открыть соседнюю вкладку браузера")
    # def open_next_tab(driver):
    #     """
    #     Перемещает "курсор" селениума на соседнюю вкладку.
    #     """
    #     wait = WebDriverWait(driver, 10)
    #     wait.until(ec.number_of_windows_to_be(2))
    #     driver.switch_to.window(driver.window_handles[1])

    # @staticmethod
    # @allure.step("Вернуться на предыдущую вкладку")
    # def back_to_prev_tab(driver):
    #     """
    #     Возвращает "курсор" селениума на предыдущую вкладку.
    #     """
    #     driver.close()
    #     driver.switch_to.window(driver.window_handles[0])
