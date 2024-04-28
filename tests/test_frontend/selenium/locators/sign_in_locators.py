from selene.support.shared.jquery_style import s
from base_page_locators import BasePageLocators

class SignInLocators(BasePageLocators):
    sign_up_btn = s("//*[@id='tabs-bui8-tab-1']")

    username = s("//*[@id='text_input_8']")
    password = s("//*[@id='text_input_9']")
    log_in_btn = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div[4]/div/button")
