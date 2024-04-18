import json
import re

import requests
import SessionService
from bs4 import BeautifulSoup

API_URL = "http://127.0.0.1:8080"


class SearchThread:
    def __init__(self, thread_json):
        self.username = thread_json["username"]
        self.link_id = thread_json["link"]["id"]
        self.link = thread_json["link"]["link"]
        self.title = thread_json["link"]["title"]
        self.platform = thread_json["link"]["platform"]
        self.date = thread_json["date"]


class Feedback:
    def __init__(self, feedback_json):
        self.username = feedback_json["username"]
        self.id = feedback_json["feedback"]["id"]
        self.user_id = feedback_json["feedback"]["user_id"]
        self.link_id = feedback_json["feedback"]["link_id"]
        self.comment = feedback_json["feedback"]["comment"]
        self.date = feedback_json["feedback"]["date"]


def register(email, username, password) -> (bool, str):
    response = requests.post(f"{API_URL}/auth/register",
                             json={"email": email, "username": username, "password": password})

    if response.status_code == 200:
        return response.json()['success'], response.json()['error']

    return None


def login(username, password):
    response = requests.post(f"{API_URL}/auth/token", data={"username": username, "password": password})
    if response.status_code == 200:
        SessionService.set_access_token(response.json()['access_token'])
        SessionService.set_refresh_token(response.json()["refresh_token"])

        return True, ""

    return False, response.json()["detail"]


def get_user_info():
    response = requests.get(f"{API_URL}/user/get_info",
                            headers={"Authorization": f"Bearer {SessionService.get_access_token()}"})
    if response.status_code == 200:
        return response.json()["success"], response.json()["user"]

    return False, response.json()["detail"]


def create_thread(link: str, title: str, platform: str, comment: str):
    payload = json.dumps({
        "link": link,
        "title": title,
        "platform": platform,
        "comment": comment
    })

    response = requests.post(f"{API_URL}/thread/create",
                             headers={"Authorization": f"Bearer {SessionService.get_access_token()}"},
                             data=payload)
    try:
        if response.json()["detail"]:
            return False, "You are not logged in :("
    except:
        pass

    return response.json()["success"], response.json()["error"]


def search(url: bool, query: str) -> [SearchThread]:
    if query:
        response = requests.get(f"{API_URL}/thread/search?url={url}&query={query}&limit=100")
    else:
        response = requests.get(f"{API_URL}/thread/search?limit=100")

    res = []
    for thread in response.json()["threads"]:
        res.append(SearchThread(thread))

    return res


def get_thread_details(link_id) -> [Feedback]:
    response = requests.get(f"{API_URL}/thread/get/{link_id}")

    res = []
    for feedback in response.json()["feedback"]:
        res.append(Feedback(feedback))

    return res


def add_feedback(link_id, comment) -> (bool, str):
    payload = json.dumps({
        "link_id": link_id,
        "comment": comment
    })

    response = requests.post(f"{API_URL}/thread/feedback/add",
                             data=payload,
                             headers={"Authorization": f"Bearer {SessionService.get_access_token()}"})

    try:
        if response.json()["detail"]:
            return False, "You are not logged in :("
    except:
        pass

    return response.json()["success"], response.json()["error"]


def edit_feedback(feedback_id, comment) -> (bool, str):
    payload = json.dumps({
        "feedback_id": feedback_id,
        "comment": comment
    })

    response = requests.post(f"{API_URL}/thread/feedback/edit",
                             data=payload,
                             headers={"Authorization": f"Bearer {SessionService.get_access_token()}"})

    return response.json()["success"], response.json()["error"]


def get_content_details_from_url(url):
    # Отправляем запрос к указанной URL и получаем содержимое страницы
    response = requests.get(url)
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        # Находим необходимые элементы на странице и извлекаем данные
        unique_id = url  # Уникальный ID можно использовать как саму URL
        platform = re.search(r'(?<=://)(.*?)(?=/|$)', url).group(0)  # Платформа извлекается из URL
        name = soup.title.text.strip()  # Название контента из заголовка страницы
        # Возвращаем полученные данные
        return platform, name
    else:
        # Если запрос неудачный, выводим сообщение об ошибке
        print("Failed to fetch content from URL:", url)
        return None
