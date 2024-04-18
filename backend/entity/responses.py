from pydantic import BaseModel
from typing import List, Optional
from backend.entity.feedback import FeedbackPage
from backend.entity.user import User
from backend.entity.thread import Thread, ThreadFeedback


class StandardResponse(BaseModel):
    success: bool
    error: str


class FeedbackListResponse(BaseModel):
    success: bool
    feedback: List[ThreadFeedback]


class FeedbackResponse(BaseModel):
    success: bool
    feedback: Optional[FeedbackPage] = None


class UserInfoResponse(BaseModel):
    success: bool
    user: User


class ThreadResponse(BaseModel):
    success: bool
    threads: Optional[List[Thread]] = None
