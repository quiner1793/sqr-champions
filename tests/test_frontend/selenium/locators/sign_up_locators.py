from locators.base_page_locators import BasePageLocators
from selene.support.shared.jquery_style import s


class SignUpLocators(BasePageLocators):
    username = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[2]/div/div[1]/div/input")  # noqa
    email = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[3]/div/div[1]/div/input")  # noqa
    password = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[4]/div/div[1]/div/input")  # noqa
    create_account = s(
        "/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[5]/div/button")  # noqa
    alert_text = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[6]/div/div/div/div/div/div")  # noqa
