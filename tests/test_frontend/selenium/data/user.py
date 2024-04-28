from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    password: str
    email: str


create_new_user = UserData(
    username="test_user", password="test_pass", email="test@mail.ru"
)
