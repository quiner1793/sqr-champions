import streamlit as st

access_token_key = "access_token"
refresh_token_key = "refresh_token"


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
