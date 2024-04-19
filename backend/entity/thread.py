from pydantic import BaseModel
from typing import Optional
from backend.entity.link import Link
from backend.entity.feedback import Feedback


class Thread(BaseModel):
    username: Optional[str]
    link: Optional[Link]
    date: Optional[str]


class ThreadFeedback(BaseModel):
    username: str
    feedback: Feedback
