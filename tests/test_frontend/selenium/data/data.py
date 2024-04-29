from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    password: str
    email: str


@dataclass
class ThreadData:
    title: str
    link: str
    feedback: str


existing_user = UserData(
    username="test", password="test", email="test@mail.ru"
)

new_user = UserData(
    username="username", password="user_password", email="user@mail.ru"
)

wrong_email_new_user = UserData(
    username="qwerty", password="user_password", email="@mail.ru"
)

not_existing_user = UserData(
    username="not_existing_user",
    password="user_password",
    email="false@mail.ru"
)

existing_thread = ThreadData(
    title="Shia LaBeouf",
    link="https://www.youtube.com/watch?v=o0u4M6vppCI",
    feedback="Testing comment"
)
