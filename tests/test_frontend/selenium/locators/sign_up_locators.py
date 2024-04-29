from locators.base_page_locators import BasePageLocators
from selene.support.shared.jquery_style import s


class SignUpLocators(BasePageLocators):
    username = s("//*[@id='text_input_3']")
    email = s("//*[@id='text_input_4']")
    password = s("//*[@id='text_input_5']")
    create_account = s(
        "/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[5]/div/button") # noqa
    alert = s("//*[@id='tabs-bui2-tabpanel-1']/div/div/div/div[6]/div/div")
    alert_text = s(
        "//*[@id='tabs-bui2-tabpanel-1']/div/div/div/div[6]/div/div/div/div/div/div") # noqa
