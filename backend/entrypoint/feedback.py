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
from backend.entity.responses import FeedbackListResponse
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
    linkGw = LinkGw(request.app.state.db)
    feedbackGw = FeedbackGw(request.app.state.db)

    user_data = await userGw.get_user_by_username(user.username)
    link_data = await linkGw.get_link_data_by_link(body.link)

    if link_data is None:
        try:
            link_id = await linkGw.add_link(body)
        except Exception as e:
            logging.error(f"error in inserting link: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        link_id = link_data.id
    try:
        await feedbackGw.add_feedback(Feedback(user_id=user_data.id,
                                               link_id=link_id,
                                               comment=body.comment))
    except Exception as e:
        logging.error(f"error in inserting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return StandardResponse(success=True, error="")


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


@router.get("/search/",
            summary="search feedback",
            response_model=FeedbackListResponse)
async def search_feedback(
        query: str,
        url: bool,
        request: Request,
) -> FeedbackListResponse:
    feedbackGw = FeedbackGw(request.app.state.db)
    linkGw = LinkGw(request.app.state.db)

    if url:
        query = query.replace("%3A", ":")
        query = query.replace("%2F", "/")

        # Search link by url
        link_data = await linkGw.get_link_data_by_link(query)
        if link_data is None:
            return FeedbackListResponse(success=False, feedback=[])
        try:
            result = await feedbackGw.get_feedback_list(link_data.id)
        except Exception as e:
            logging.error(f"error in getting link feedback: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return FeedbackListResponse(success=True, feedback=result)
    else:
        # Search urls by matches in platform or title strings
        links = await linkGw.get_links_by_query(query)
        if not links:
            return FeedbackListResponse(success=False, feedback=[])
        results = []
        for link in links:
            try:
                result = await feedbackGw.get_feedback_list(link.id)
                results.extend(result)
            except Exception as e:
                logging.error(f"error in getting feedback: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return FeedbackListResponse(success=True, feedback=results)
