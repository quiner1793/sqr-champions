from locators.base_page_locators import BasePageLocators
from selene.support.shared.jquery_style import s


class LoggedInLocators(BasePageLocators):
    created_profile_title = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[1]/div") # noqa
