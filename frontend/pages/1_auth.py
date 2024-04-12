import streamlit as st
import requests

API_URL = "http://your-api-url.com"


def login(username, password):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()['token']
    return None


def register(username, password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()['token']
    return None


st.title('Comment Hub')

if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None

tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

with tab1:
    st.header("Sign In")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Log in")

    if login_button:
        token = login(login_username, login_password)
        if token:
            st.session_state['jwt_token'] = token
            st.success("Вы успешно вошли!")
            st.write("Ваш токен: ", token)
        else:
            st.error("Неверное имя пользователя или пароль")

with tab2:
    st.header("Sign Up")
    reg_username = st.text_input("Username", key="reg_username")
    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_button = st.button("Create account")

    if reg_button:
        token = register(reg_username, reg_password)
        if token:
            st.session_state['jwt_token'] = token
            st.success("Вы успешно зарегистрировались!")
            st.write("Ваш токен: ", token)
        else:
            st.error("Такой пользователь уже существует или произошла ошибка на сервере")
