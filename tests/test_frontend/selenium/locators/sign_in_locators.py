from locators.base_page_locators import BasePageLocators
from selene.support.shared.jquery_style import s


class SignInLocators(BasePageLocators):
    sign_up_btn = s("//*[@id='tabs-bui2-tab-1']")

    username = s(
        "//*[@id='tabs-bui80-tabpanel-0']/div/div/div/div[2]/div/div[1]/div/input") # noqa
    password = s(
        "//*[@id='tabs-bui80-tabpanel-0']/div/div/div/div[3]/div/div[1]/div/input") # noqa
    log_in_btn = s(
        "/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div[4]/div/button") # noqa

    alert = s("//*[@id='tabs-bui2-tabpanel-0']/div/div/div/div[5]/div/div")
