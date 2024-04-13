from pydantic import BaseModel
from typing import List, Optional
from backend.entity.feedback import Feedback
from backend.entity.feedback import FeedbackPage
from backend.entity.user import User


class StandardResponse(BaseModel):
    success: bool
    error: str


class FeedbackListResponse(BaseModel):
    success: bool
    feedback: List[Feedback]


class FeedbackResponse(BaseModel):
    success: bool
    feedback: Optional[FeedbackPage] = None


class UserInfoResponse(BaseModel):
    success: bool
    user: User
