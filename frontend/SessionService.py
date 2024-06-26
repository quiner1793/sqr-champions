from enum import Enum
from typing import Optional
import streamlit as st
import NetworkService


class MainPageState(Enum):
    SEARCH = 0
    NEW_THREAD = 1
    THREAD_DETAIL = 2


main_page_state = MainPageState.SEARCH

searchResults: [NetworkService.SearchThread] = NetworkService.search(False, "")

access_token_key = "access_token"
refresh_token_key = "refresh_token"
id_key = "user_id"


class Thread:
    comments: [NetworkService.Feedback] = []

    def __init__(self, link_id: int, url: str, platform: str, content_title: str, author: str, date: str):
        self.link_id = link_id
        self.url = url
        self.platform = platform
        self.content_title = content_title
        self.author = author
        self.date = date


selectedThread: Optional[Thread] = None


def set_access_token(token: str):
    st.session_state[access_token_key] = token


def set_refresh_token(token: str):
    st.session_state[refresh_token_key] = token


def set_id(user_id: int):
    st.session_state[id_key] = user_id


def get_id() -> int:
    if id_key in st.session_state:
        return st.session_state[id_key]


def is_access_token_valid():
    pass


def is_refresh_token_valid():
    pass


def get_access_token():
    if access_token_key in st.session_state:
        return st.session_state[access_token_key]

    return None


def get_refresh_token():
    if refresh_token_key in st.session_state:
        return st.session_state[refresh_token_key]

    return None
