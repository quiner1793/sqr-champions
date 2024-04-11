from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class AddFeedbackRequest(BaseModel):
    link: str
    title: str
    platform: str
    comment: str
