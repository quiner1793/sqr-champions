import requests
from SessionService import *

API_URL = "http://127.0.0.1:8080"


def register(email, username, password) -> (bool, str):
    response = requests.post(f"{API_URL}/auth/register",
                             json={"email": email, "username": username, "password": password})

    if response.status_code == 200:
        return response.json()['success'], response.json()['error']

    return None


def login(username, password):
    response = requests.post(f"{API_URL}/auth/token", data={"username": username, "password": password})
    if response.status_code == 200:
        set_access_token(response.json()['access_token'])
        set_refresh_token(response.json()["refresh_token"])

        return True, ""

    return False, response.json()["detail"]


def get_user_info():
    response = requests.get(f"{API_URL}/user/get_info", headers={"Authorization": f"Bearer {get_access_token()}"})
    if response.status_code == 200:
        return response.json()["success"], response.json()["user"]

    return False, response.json()["detail"]
