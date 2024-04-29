import pytest
from httpx import AsyncClient


class TestApiUser:
    @pytest.mark.asyncio
    async def test_successful_get_info(self, test_app, test_user_data):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.post(
                "/auth/token", data=test_user_data
            )
            assert response.status_code == 200
            token = response.json()["access_token"]
            response = await client.get(
                "/user/get_info", headers={"Authorization": f"Bearer {token}"}
            )
            test_user_data["id"] = 1
            assert response.status_code == 200
            print(response.json()["user"])
            user_data = response.json()["user"]
            assert user_data == test_user_data

    @pytest.mark.asyncio
    async def test_get_info_unauthorized(self, test_app):
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            response = await client.get(
                "/user/get_info", headers={"Authorization": "Bearer abc"}
            )
            assert response.status_code == 401
            assert response.json()["detail"] == "Invalid token"
