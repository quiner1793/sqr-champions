from pydantic import BaseModel
from typing import List, Optional
from backend.entity.feedback import FeedbackPage
from backend.entity.user import User
from backend.entity.thread import Thread, ThreadFeedback
from backend.entity.token import Token


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


common_responses = {
    "401": {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated"
                }
            },
        },
        "description": "Not authenticated",
    },
    "403": {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Forbidden"
                }
            },
        },
        "description": "Forbidden",
    },
    "500": {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Internal server error"
                }
            },
        },
        "description": "Internal server error",
    },
}

login_responses = {
    200: {
        "model": Token,
        "description": "Returns token information",
    },
    400: {
        "content": {"application/json": {"example": {
            "detail": "Invalid username or password"}}},
        "description":
            "Invalid username or password",
    },
    500: common_responses["500"],
}

register_responses = {
    200: {
        "model": StandardResponse,
        "description": "Register user",
    },
    409: {
        "content": {"application/json": {"example": {
            "detail": "Person with such login/email is already registered"}}},
        "description": "Person with such login/email is already registered",
    },
    422: {
        "content": {"application/json": {"example": {
            "detail": "Invalid email"}}},
        "description": "Invalid email",
    },
    500: common_responses["500"],
}

user_responses = {
    200: {
        "model": UserInfoResponse,
        "description": "User information",
    },
    401: common_responses["401"],
    500: common_responses["500"],
}

search_thread_responses = {
    200: {
        "model": ThreadResponse,
        "description": "Get list of threads",
    },
    500: common_responses["500"],
}

get_thread_responses = {
    200: {
        "model": FeedbackListResponse,
        "description": "Get thread",
    },
    500: common_responses["500"],
}

create_thread_responses = {
    200: {
        "model": ThreadResponse,
        "description": "Add thread",
    },
    401: common_responses["401"],
    409: {
        "content": {"application/json": {"example": {
            "detail": "Such thread already exists"}}},
        "description": "Such thread already exists",
    },
    500: common_responses["500"],
}

add_feedback_responses = {
    200: {
        "model": StandardResponse,
        "description": "Add feedback",
    },
    401: common_responses["401"],
    500: common_responses["500"],
}

get_feedback_responses = {
    200: {
        "model": FeedbackResponse,
        "description": "Get feedback",
    },
    500: common_responses["500"],
}

edit_feedback_responses = {
    200: {
        "model": StandardResponse,
        "description": "Edit feedback",
    },
    401: common_responses["401"],
    403: common_responses["403"],
    500: common_responses["500"],
}
