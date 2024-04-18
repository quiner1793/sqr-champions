from pydantic import BaseModel
from backend.entity.link import Link
from backend.entity.feedback import Feedback


class Thread(BaseModel):
    username: str
    link: Link
    date: str


class ThreadFeedback(BaseModel):
    username: str
    feedback: Feedback
