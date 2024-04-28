import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st  # noqa: E402
import frontend.NetworkService  # noqa: E402
import frontend.SessionService  # noqa: E402


def auth_ui():
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
            tokens = frontend.NetworkService.login(login_username, login_password)
            if tokens[0]:
                st.rerun()
            else:
                st.error(tokens[1])

    with tab2:
        st.header("Sign Up")
        reg_username = st.text_input("Username", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_button = st.button("Create account")

        if reg_button:
            result = frontend.NetworkService.register(email=reg_email, username=reg_username, password=reg_password)
            if result[0]:
                st.success("You have successfully registered!")

                tokens = frontend.NetworkService.login(reg_username, reg_password)
                if tokens[0]:
                    st.rerun()
                else:
                    st.error(tokens[1])

            else:
                st.error(result[1])


def profile_ui():
    st.title('Profile')

    data = frontend.NetworkService.get_user_info()
    frontend.SessionService.set_id(data[1]["id"])
    if data[0]:
        username = data[1]["username"]
        password = data[1]["password"]
        email = data[1]["email"]

        st.write("### Username:")
        st.write(username)

        st.write("### Password:")
        st.write(password)

        st.write("### Email:")
        st.write(email)
    else:
        st.error(data[1])


if frontend.SessionService.get_access_token():
    profile_ui()
else:
    auth_ui()
