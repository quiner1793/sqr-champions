from typing import Optional

from fastapi import APIRouter

from backend.entity import requests
from backend.entity.feedback import Feedback
from backend.entity.user import User
from backend.gateway.feedback_gw import FeedbackGw
from backend.gateway.link_gw import LinkGw
from fastapi import Request, status, HTTPException
from backend.entity.responses import ThreadResponse
from backend.entity.responses import search_thread_responses
from backend.entity.responses import get_thread_responses
from backend.entity.responses import create_thread_responses
from backend.entity.responses import FeedbackListResponse
import logging
from fastapi import Security
from backend.entity.thread import Thread, ThreadFeedback
from backend.entity.link import Link
from backend.gateway.user_gw import UserGw
from backend.utils.auth import get_current_user

router = APIRouter()


@router.get("/search",
            summary="search for threads",
            response_model=ThreadResponse,
            responses={**search_thread_responses})
async def search(
        request: Request,
        url: Optional[bool] = None,
        query: Optional[str] = None,
        limit: Optional[int] = 10,
) -> ThreadResponse:
    link_gw = LinkGw(request.app.state.db)
    feedback_gw = FeedbackGw(request.app.state.db)
    user_gw = UserGw(request.app.state.db)

    if query is None:
        links = await link_gw.get_latest(limit)
        result = []
        if len(links) > 0:
            for link in links:
                feedback = await feedback_gw.get_first_feedback(link.id)
                username = await user_gw.get_username_by_id(feedback.user_id)
                result.append(Thread(username=username,
                                     link=link,
                                     date=feedback.date))

        return ThreadResponse(success=len(result) > 0, threads=result)

    if url:
        query = query.replace("%3A", ":")
        query = query.replace("%2F", "/")

        # Search link by url
        try:
            link_data = await link_gw.get_link_data_by_link(query)

            if link_data is None:
                return ThreadResponse(success=False, threads=[])

            feedback = await feedback_gw.get_first_feedback(link_data.id)
            username = await user_gw.get_username_by_id(feedback.user_id)

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
            links = await link_gw.get_links_by_query(query)
            result = []
            for link in links:
                feedback = await feedback_gw.get_first_feedback(link.id)
                username = await user_gw.get_username_by_id(feedback.user_id)

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
            response_model=FeedbackListResponse,
            responses={**get_thread_responses})
async def get(
        request: Request,
        link_id: int,
) -> FeedbackListResponse:
    feedback_gw = FeedbackGw(request.app.state.db)
    user_gw = UserGw(request.app.state.db)
    try:
        feedback_list = await feedback_gw.get_feedback_list(link_id)
        result = []
        for feedback in feedback_list:
            username = await user_gw.get_username_by_id(feedback.user_id)
            result.append(ThreadFeedback(username=username, feedback=feedback))
        return FeedbackListResponse(success=len(feedback_list) > 0,
                                    feedback=result)

    except Exception as e:
        logging.error(f"error in getting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/create", summary="create thread",
             response_model=ThreadResponse,
             responses={**create_thread_responses})
async def create(
        body: requests.CreateThreadRequest,
        request: Request,
        user: User = Security(get_current_user)
) -> ThreadResponse:
    user_gw = UserGw(request.app.state.db)
    link_gw = LinkGw(request.app.state.db)
    feedback_gw = FeedbackGw(request.app.state.db)

    user_data = await user_gw.get_user_by_username(user.username)
    link_data = await link_gw.get_link_data_by_link(body.link)

    if link_data is None:
        try:
            link_id = await link_gw.add_link(body)
            date = await feedback_gw.add_feedback(Feedback(
                user_id=user_data.id,
                link_id=link_id,
                comment=body.comment)
            )
            return ThreadResponse(success=True,
                                  threads=[Thread(username=user_data.username,
                                                  link=Link(id=link_id,
                                                            link=body.link,
                                                            title=body.title,
                                                            platform=body.platform),  # noqa: E501
                                                  date=date)])

        except Exception as e:
            logging.error(f"error in creating thread: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Such thread already exists"
        )
