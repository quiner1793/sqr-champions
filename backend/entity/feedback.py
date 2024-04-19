from pydantic import BaseModel
from typing import Optional
from backend.entity.link import Link


class Feedback(BaseModel):
    id: Optional[int] = None
    user_id: int
    link_id: int
    comment: str
    date: Optional[str] = None


class FeedbackPage(BaseModel):
    id: Optional[int] = None
    username: str
    link: Link
    comment: str
    date: Optional[str] = None
