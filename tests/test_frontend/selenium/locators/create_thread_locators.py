from selene.support.shared.jquery_style import s
from base_page_locators import BasePageLocators

class CreateThreadLocators(BasePageLocators):
    url = s("//*[@id='text_input_2']")
    feedback = s("//*[@id='text_area_3']")
    create_btn = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[5]/div/button")
    back = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[1]/div/button")
    