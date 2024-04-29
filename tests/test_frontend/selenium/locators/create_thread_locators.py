from selene.support.shared.jquery_style import s
from locators.base_page_locators import BasePageLocators


class CreateThreadLocators(BasePageLocators):
    url = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[3]/div/div[1]/div/input")  # noqa
    feedback = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[4]/div/div[1]/div/div/textarea")  # noqa
    create_btn = s(
        "/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[5]/div/button")  # noqa
    back = s(
        "/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[1]/div/button")  # noqa
