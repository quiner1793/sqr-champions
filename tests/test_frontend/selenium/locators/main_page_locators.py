from selene.support.shared.jquery_style import s
from base_page_locators import BasePageLocators

class MainPageLocators(BasePageLocators):
    enter_query = s("//*[@id='text_input_1']")
    search_btn = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[3]/div/button")
    searching_result = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[4]/div/div")
    create_thread_btn = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/button")
