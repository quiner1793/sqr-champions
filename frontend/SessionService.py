from enum import Enum

import streamlit as st
from NetworkService import search

access_token_key = "access_token"
refresh_token_key = "refresh_token"


class MainPageState(Enum):
    SEARCH = 0
    NEW_THREAD = 1
    THREAD_DETAIL = 2


main_page_state = MainPageState.THREAD_DETAIL

searchResults = search(False, "")


class Thread:
    comments = []

    def __init__(self, link_id: int, url: str, platform: str, content_title: str, author: str, date: str):
        self.link_id = link_id
        self.url = url
        self.platform = platform
        self.content_title = content_title
        self.author = author
        self.date = date


selectedThread: Thread = None


def set_access_token(token: str):
    st.session_state[access_token_key] = token


def set_refresh_token(token: str):
    st.session_state[refresh_token_key] = token


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
