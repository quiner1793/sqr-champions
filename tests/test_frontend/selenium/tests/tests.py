from data.data import (existing_thread, existing_user, new_user,
                       not_existing_user, wrong_email_new_user)
from locators.logged_in_locators import LoggedInLocators
from locators.sign_in_locators import SignInLocators
from locators.sign_up_locators import SignUpLocators
from locators.thread_page_locators import ThreadPageLocators
from pages.sign_in_page import SignInPage
from pages.sign_up_page import SignUpPage
from pages.thread_page import ThreadPage
from selene import be, query


class TestMainPage:
    def test_search(self, open_main_page_function, main_page):
        main_page.enter_query(existing_thread.link)
        main_page.search()
        assert main_page.first_element_search.should(be.visible)

    def test_search_by_platform(self, open_main_page_function, main_page):
        main_page.enter_query("youtube")
        main_page.search()
        assert main_page.first_element_search.should(be.visible)


class TestAddFeedback:
    def test_add_feedback(self, open_main_page_function, main_page):
        main_page.open_profile()
        SignInPage.enter_username(existing_user.username)
        SignInPage.enter_password(existing_user.password)
        main_page.open_comment_hub()
        assert main_page.first_element_search.should(be.visible)
        main_page.open_thread_page()
        assert ThreadPageLocators.feedback.should(be.visible)
        ThreadPage.enter_feedback("New feedback")
        ThreadPage.submit()
        assert ThreadPageLocators.first_feedback.should(be.visible)
        assert ThreadPageLocators.first_feedback.get(
            query.text) == "New feedback"

    def test_add_feedback_unauthorized(self, open_main_page_function, main_page):  # noqa
        assert main_page.first_element_search.should(be.visible)
        main_page.open_thread_page()
        assert ThreadPageLocators.feedback.should(be.visible)
        ThreadPage.enter_feedback("New feedback")
        ThreadPage.submit()
        assert ThreadPageLocators.alert.should(be.visible)
        assert ThreadPageLocators.alert.get(
            query.text) == "You are not logged in :("


class TestRegistration:
    def test_register(self, open_main_page_function, main_page):
        main_page.open_profile()
        SignInPage.open_sign_up_page()
        SignUpPage.enter_username(new_user.username)
        SignUpPage.enter_email(new_user.email)
        SignUpPage.enter_password(new_user.password)
        SignUpPage.create_account()
        assert SignUpLocators.create_account.should(be.not_.visible)
        assert LoggedInLocators.created_profile_title.should(be.visible)

    def test_register_with_username_conflict(self, open_main_page_function, main_page): # noqa
        main_page.open_profile()
        SignInPage.open_sign_up_page()
        SignUpPage.enter_username(existing_user.username)
        SignUpPage.enter_email(existing_user.email)
        SignUpPage.enter_password(existing_user.password)
        SignUpPage.create_account()
        assert SignUpLocators.create_account.should(be.visible)
        assert SignUpLocators.alert.should(be.visible)
        assert SignUpLocators.alert_text.get(
            query.text) == "Person with such username is already registered"

    def test_register_with_wrong_email(self, open_main_page_function, main_page): # noqa
        main_page.open_profile()
        SignInPage.open_sign_up_page()
        SignUpPage.enter_username(wrong_email_new_user.username)
        SignUpPage.enter_email(wrong_email_new_user.email)
        SignUpPage.enter_password(wrong_email_new_user.password)
        SignUpPage.create_account()
        assert SignUpLocators.create_account.should(be.visible)
        assert SignUpLocators.alert.should(be.visible)
        assert SignUpLocators.alert_text.get(
            query.text) == "Invalid email"


class TestLogin:
    def test_login(self, open_main_page_function, main_page):
        main_page.open_profile()
        SignInPage.enter_username(existing_user.username)
        SignInPage.enter_password(existing_user.password)
        SignInPage.log_in()
        assert SignInPage.log_in.should(be.not_.visible)
        assert LoggedInLocators.created_profile_title.should(be.visible)

    def test_wrong_login(self, open_main_page_function, main_page):
        main_page.open_profile()
        SignInPage.enter_username(not_existing_user.username)
        SignInPage.enter_password(not_existing_user.password)
        SignInPage.log_in()
        assert SignInLocators.log_in_btn.should(be.visible)
        assert SignInLocators.alert.get(
            query.text) == "Invalid username or password"
