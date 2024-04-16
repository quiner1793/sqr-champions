from fastapi import APIRouter

from backend.gateway.feedback_gw import FeedbackGw
from backend.gateway.link_gw import LinkGw
from backend.gateway.user_gw import UserGw
from backend.utils.auth import get_current_user
from fastapi import Security
from fastapi import Request, status, HTTPException
from backend.entity.user import User
from backend.entity import requests
from backend.entity.feedback import Feedback
from backend.entity.feedback import FeedbackPage
from backend.entity.responses import StandardResponse
from backend.entity.responses import FeedbackResponse
import logging

router = APIRouter()


@router.post("/add", summary="add feedback", response_model=StandardResponse)
async def add_feedback(
        body: requests.AddFeedbackRequest,
        request: Request,
        user: User = Security(get_current_user)
) -> StandardResponse:
    userGw = UserGw(request.app.state.db)
    feedbackGw = FeedbackGw(request.app.state.db)

    user_data = await userGw.get_user_by_username(user.username)

    try:
        await feedbackGw.add_feedback(Feedback(user_id=user_data.id,
                                               link_id=body.link_id,
                                               comment=body.comment))
        return StandardResponse(success=True, error="")

    except Exception as e:
        logging.error(f"error in inserting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/get/{feedback_id}",
            summary="get feedback",
            response_model=FeedbackResponse)
async def get_feedback(
        feedback_id: int,
        request: Request,
) -> FeedbackResponse:
    feedbackGw = FeedbackGw(request.app.state.db)
    linkGw = LinkGw(request.app.state.db)
    userGw = UserGw(request.app.state.db)
    try:
        feedback = await feedbackGw.get_feedback_by_id(feedback_id)
        if feedback is None:
            return FeedbackResponse(success=False, feedback=feedback)
        username = await userGw.get_username_by_id(feedback.user_id)
        link = await linkGw.get_link_data_by_link_id(feedback.link_id)
        feedbackPage = FeedbackPage(
            id=feedback.id,
            username=username,
            link=link,
            comment=feedback.comment,
            date=feedback.date)
    except Exception as e:
        logging.error(f"error in getting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return FeedbackResponse(success=True, feedback=feedbackPage)


@router.post("/edit", summary="edit feedback", response_model=StandardResponse)
async def edit_feedback(
        body: requests.EditFeedbackRequest,
        request: Request,
        user: User = Security(get_current_user)
) -> StandardResponse:
    feedbackGw = FeedbackGw(request.app.state.db)
    userGw = UserGw(request.app.state.db)

    feedback = await feedbackGw.get_feedback_by_id(body.feedback_id)
    user_data = await userGw.get_user_by_username(user.username)
    if feedback.user_id != user_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    try:
        await feedbackGw.update_feedback(body.feedback_id, body.comment)
        return StandardResponse(success=True, error="")

    except Exception as e:
        logging.error(f"error in editing feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
