from locators.base_page_locators import BasePageLocators
from selene.support.shared.jquery_style import s


class MainPageLocators(BasePageLocators):
    enter_query = s("//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[2]/div/div[1]/div/input")  # noqa
    search_btn = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[3]/div/button")  # noqa
    searching_result = s("/html/body/div/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[4]/div/div")  # noqa
    create_thread_btn = s("//*button[2]")  # noqa
    first_element_search_title = s("//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[4]/div/div/div")  # noqa
    first_element_show_btn = s("//*[@id='root']/div[1]/div[1]/div/div/div/section[2]/div[1]/div/div/div/div[7]/div[2]/div/div/div/div/div/button")  # noqa
