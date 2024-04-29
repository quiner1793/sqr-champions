from locators.base_page_locators import BasePageLocators
from selene.support.shared.jquery_style import s


class ThreadPageLocators(BasePageLocators):
    thread_title = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div/div/div") # noqa
    feedback = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[7]/div/div[1]/div/div/textarea") # noqa
    submit = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[8]/div/button") # noqa
    first_feedback = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[11]/div/div/p/text()[2]") # noqa

    alert = s(
        "//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[9]/div/div/div/div/div/div") # noqa
