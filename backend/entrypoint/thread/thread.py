from typing import Optional

from fastapi import APIRouter

from backend.entity import requests
from backend.entity.feedback import Feedback
from backend.entity.user import User
from backend.gateway.feedback_gw import FeedbackGw
from backend.gateway.link_gw import LinkGw
from fastapi import Request, status, HTTPException
from backend.entity.responses import ThreadResponse, StandardResponse
from backend.entity.responses import FeedbackListResponse
import logging
from fastapi import Security
from backend.entity.thread import Thread, ThreadFeedback

from backend.gateway.user_gw import UserGw
from backend.utils.auth import get_current_user

router = APIRouter()


@router.get("/search",
            summary="search for threads",
            response_model=ThreadResponse)
async def search(
        request: Request,
        url: Optional[bool] = None,
        query: Optional[str] = None,
        limit: Optional[int] = 10,
) -> ThreadResponse:
    linkGw = LinkGw(request.app.state.db)
    feedbackGw = FeedbackGw(request.app.state.db)
    userGw = UserGw(request.app.state.db)

    if query is None:
        links = await linkGw.get_latest(limit)
        result = []
        if len(links) > 0:
            for link in links:
                feedback = await feedbackGw.get_first_feedback(link.id)
                username = await userGw.get_username_by_id(feedback.user_id)
                result.append(Thread(username=username,
                                     link=link,
                                     date=feedback.date))

        return ThreadResponse(success=len(result) > 0, threads=result)

    if url:
        query = query.replace("%3A", ":")
        query = query.replace("%2F", "/")

        # Search link by url
        try:
            link_data = await linkGw.get_link_data_by_link(query)

            if link_data is None:
                return ThreadResponse(success=False, threads=[])

            feedback = await feedbackGw.get_first_feedback(link_data.id)
            username = await userGw.get_username_by_id(feedback.user_id)

        except Exception as e:
            logging.error(f"error in getting link: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return ThreadResponse(success=True,
                              threads=[Thread(username=username,
                                              link=link_data,
                                              date=feedback.date)])
    else:
        try:
            # Search urls by matches in platform or title strings
            links = await linkGw.get_links_by_query(query)
            result = []
            for link in links:
                feedback = await feedbackGw.get_first_feedback(link.id)
                username = await userGw.get_username_by_id(feedback.user_id)

                result.append(Thread(username=username,
                                     link=link,
                                     date=feedback.date))

            return ThreadResponse(success=len(links) > 0, threads=result)

        except Exception as e:
            logging.error(f"error in getting links: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@router.get("/get/{link_id}",
            summary="get thread",
            response_model=FeedbackListResponse)
async def get(
        request: Request,
        link_id: int,
) -> FeedbackListResponse:
    feedbackGw = FeedbackGw(request.app.state.db)
    userGw = UserGw(request.app.state.db)
    try:
        feedback_list = await feedbackGw.get_feedback_list(link_id)
        result = []
        for feedback in feedback_list:
            username = await userGw.get_username_by_id(feedback.user_id)
            result.append(ThreadFeedback(username=username, feedback=feedback))
        return FeedbackListResponse(success=len(feedback_list) > 0,
                                    feedback=result)

    except Exception as e:
        logging.error(f"error in getting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/create", summary="create thread",
             response_model=StandardResponse)
async def create(
        body: requests.CreateThreadRequest,
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
            await feedbackGw.add_feedback(Feedback(user_id=user_data.id,
                                                   link_id=link_id,
                                                   comment=body.comment))
            return StandardResponse(success=True, error="")

        except Exception as e:
            logging.error(f"error in creating thread: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    else:
        return StandardResponse(success=False,
                                error="Such thread already exist")
