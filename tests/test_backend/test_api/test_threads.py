import datetime
import json
from zoneinfo import ZoneInfo
import pytest

from httpx import AsyncClient
from backend.gateway.feedback_gw import FEEDBACK_DATETIME_FORMAT


class TestTread:
    @pytest.mark.asyncio
    async def test_create_thread(self, test_app, link_data, test_user_data):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post("/auth/token", data=test_user_data)
            token = response.json()["access_token"]
            payload = json.dumps(link_data)
            link_data["id"] = 2
            del link_data["comment"]
            response = await client.post(
                "/thread/create",
                headers={"Authorization": f"Bearer {token}"},
                data=payload,
            )
            assert response.status_code == 200
            threads = response.json()["threads"]
            assert len(threads) == 1
            thread = threads[0]
            assert (
                thread["username"] == "test_user"
                and thread["link"] == link_data
                and datetime.datetime.strptime(
                    thread["date"], FEEDBACK_DATETIME_FORMAT)
                < datetime.datetime.now(tz=ZoneInfo('Europe/Moscow'))
            )

    @pytest.mark.asyncio
    async def test_create_thread_on_exising_link(
        self, test_app, test_link_data, test_user_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post("/auth/token", data=test_user_data)
            token = response.json()["access_token"]
            payload = json.dumps(test_link_data)
            response = await client.post(
                "/thread/create",
                headers={"Authorization": f"Bearer {token}"},
                data=payload,
            )
            assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_search_with_url(
        self, test_app, test_link_data, test_feedback_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            query = test_link_data["link"]
            query = query.replace(":", "%3A")
            query = query.replace("/", "%2F")
            url = True
            response = await client.get(
                f"/thread/search?url={url}&query={query}&limit=100"
            )
            expected_feedback_data = {
                "username": "test_user",
                "link": {
                    "id": 1,
                    "link": test_link_data["link"],
                    "title": test_link_data["title"],
                    "platform": test_link_data["platform"],
                },
                "date": test_feedback_data["date"],
            }
            assert response.status_code == 200
            threads = response.json()["threads"]
            assert len(threads) == 1 and threads[0] == expected_feedback_data

    @pytest.mark.asyncio
    async def test_search_with_query(
        self, test_app, test_link_data, test_feedback_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            query = test_link_data["title"]
            url = False
            response = await client.get(
                f"/thread/search?url={url}&query={query}&limit=100"
            )
            expected_feedback_data = {
                "username": "test_user",
                "link": {
                    "id": 1,
                    "link": test_link_data["link"],
                    "title": test_link_data["title"],
                    "platform": test_link_data["platform"],
                },
                "date": test_feedback_data["date"],
            }
            assert response.status_code == 200
            threads = response.json()["threads"]
            assert len(threads) == 1 and threads[0] == expected_feedback_data

    @pytest.mark.asyncio
    async def test_search_no_query(
        self, test_app, test_link_data, test_feedback_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            query = ""
            url = False
            response = await client.get(
                f"/thread/search?url={url}&query={query}&limit=100"
            )
            assert response.status_code == 200
            expected_feedback_data = {
                "username": "test_user",
                "link": {
                    "id": 1,
                    "link": test_link_data["link"],
                    "title": test_link_data["title"],
                    "platform": test_link_data["platform"],
                },
                "date": test_feedback_data["date"],
            }
            threads = response.json()["threads"]
            assert len(threads) == 1 and threads[0] == expected_feedback_data

    @pytest.mark.asyncio
    async def test_get_feedback_list(
        self, test_app, test_link_data, test_feedback_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.get("thread/get/1")
            assert response.status_code == 200
            print(response.json())
            feedbacks = response.json()["feedback"]
            test_feedback_data["id"] = 1
            assert len(feedbacks) == 1 and feedbacks[0] == {
                "username": "test_user",
                "feedback": test_feedback_data,
            }

    @pytest.mark.asyncio
    async def test_get_feedback_list_wrong_id(
        self, test_app, test_link_data, test_feedback_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.get("thread/get/2")
            assert response.status_code == 200
            assert (
                response.json()["success"] is False
                and len(response.json()["feedback"]) == 0
            )


class TestFeedback:
    @pytest.mark.asyncio
    async def test_add_feedback(self, test_app, test_user_data):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            payload = {"link_id": 1, "comment": "new comment"}
            response = await client.post("/auth/token", data=test_user_data)
            token = response.json()["access_token"]
            response = await client.post(
                "/thread/feedback/add",
                data=json.dumps(payload),
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 200 and response.json()["success"]

    @pytest.mark.asyncio
    async def test_add_feedback_unauthorized(self, test_app, test_user_data):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            payload = {"link_id": 2, "comment": "new comment"}
            response = await client.post(
                "/thread/feedback/add",
                data=json.dumps(payload),
                headers={"Authorization": "Bearer abc"},
            )
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_feedback(
        self, test_app, test_feedback_data, test_link_data, test_user_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.get(
                "/thread/feedback/get/1",
            )
            assert response.status_code == 200
            assert response.json()["feedback"] == {
                "id": 1,
                "username": test_user_data["username"],
                "link": {
                    "id": 1,
                    "link": test_link_data["link"],
                    "title": test_link_data["title"],
                    "platform": test_link_data["platform"],
                },
                "comment": test_feedback_data["comment"],
                "date": test_feedback_data["date"],
            }

    @pytest.mark.asyncio
    async def test_get_not_existing_feedback(
        self, test_app, test_feedback_data, test_link_data, test_user_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.get(
                "/thread/feedback/get/2",
            )
            assert response.status_code == 200
            assert response.json()["success"] is False

    @pytest.mark.asyncio
    async def test_edit_feedback(
        self, test_app, test_feedback_data, test_link_data, test_user_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post("/auth/token", data=test_user_data)
            token = response.json()["access_token"]
            payload = json.dumps(
                {"feedback_id": 1, "comment": "some new comment"})

            response = await client.post(
                "/thread/feedback/edit",
                data=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 200
            assert response.json()["success"]

    @pytest.mark.asyncio
    async def test_edit_feedback_unauthorized(
        self, test_app, test_feedback_data, test_link_data, test_user_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            payload = json.dumps(
                {"feedback_id": 1, "comment": "some new comment"}
            )

            response = await client.post(
                "/thread/feedback/edit",
                data=payload,
                headers={"Authorization": "Bearer abc"},
            )
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_edit_feedback_by_wrong_user(
        self, test_app, test_feedback_data, test_link_data
    ):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            user_data = {
                "username": "username",
                "email": "a@mail.ru",
                "password": "testpassword",
            }
            response = await client.post(
                "/auth/register",
                json=user_data,
            )
            response = await client.post("/auth/token", data=user_data)
            token = response.json()["access_token"]
            payload = json.dumps(
                {"feedback_id": 1, "comment": "some new comment"}
            )

            response = await client.post(
                "/thread/feedback/edit",
                data=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 403
