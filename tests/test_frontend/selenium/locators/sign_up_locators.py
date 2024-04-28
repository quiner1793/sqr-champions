from selene.support.shared.jquery_style import s
from base_page_locators import BasePageLocators

class SignUpLocators(BasePageLocators):
        username = s("//*[@id='text_input_10']")
        email = s("//*[@id='text_input_11']")
        password = s("//*[@id='text_input_12']")
        create_account = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[4]/div/div/div/div[5]/div/button")
        