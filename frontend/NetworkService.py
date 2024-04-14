import requests

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
        return True, response.json()['access_token'], response.json()["refresh_token"]

    return False, response.json()["detail"]
