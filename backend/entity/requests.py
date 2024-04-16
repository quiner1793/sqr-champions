from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class CreateThreadRequest(BaseModel):
    link: str
    title: str
    platform: str
    comment: str


class AddFeedbackRequest(BaseModel):
    link_id: int
    comment: str


class EditFeedbackRequest(BaseModel):
    feedback_id: int
    comment: str
