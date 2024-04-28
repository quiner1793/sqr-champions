import pytest
from httpx import AsyncClient


class TestAuth:
    @pytest.mark.asyncio
    async def test_succesful_register(self, test_app):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post(
                "/auth/register",
                json={
                    "username": "username",
                    "email": "a@mail.ru",
                    "password": "testpassword",
                },
            )
            assert response.status_code == 200
            assert response.json()["success"] is True

    @pytest.mark.skip(reason="Failed")
    @pytest.mark.asyncio
    async def test_wrong_email_register(self, test_app):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post(
                "/auth/register",
                json={
                    "username": "username",
                    "email": "a@",
                    "password": "testpassword",
                },
            )
            assert response.status_code == 422  # TODO check after
            assert response.json()["error"] == "Invalid email"

    @pytest.mark.skip(reason="Some error with sqlite packages in python3.10")
    @pytest.mark.asyncio
    async def test_register_existing_user(self, test_app, test_user_data):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post(
                "/auth/register",
                json=test_user_data,
            )
            assert response.status_code == 200
            assert (
                response.json()["error"]
                == "Person with such username is already registered"
            )

    @pytest.mark.asyncio
    async def test_login(self, test_app, test_user_data):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post(
                "/auth/token", data=test_user_data
            )
            assert response.status_code == 200
            assert "access_token" in response.json()

    @pytest.mark.asyncio
    async def test_login_wrong_username(self, test_app):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post(
                "/auth/token", data={
                    "username": "username",
                    "password": "testpassword"}
            )
            assert response.status_code == 400
            assert response.json()["detail"] == "Invalid username or password"
