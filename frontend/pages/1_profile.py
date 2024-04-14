import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from frontend.NetworkService import *
from frontend.SessionService import *


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
            tokens = login(login_username, login_password)
            if tokens[0]:
                set_access_token(tokens[1])
                set_refresh_token(tokens[2])

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
            result = register(email=reg_email, username=reg_username, password=reg_password)
            if result[0]:

                set_access_token(result)
                st.success("You have successfully registered!")

                tokens = login(reg_username, reg_password)
                if tokens[0]:
                    set_access_token(tokens[1])
                    set_refresh_token(tokens[2])

                    st.rerun()
                else:
                    st.error(tokens[1])

            else:
                st.error(result[1])


def profile_ui():
    st.title('Profile')


if get_access_token():
    profile_ui()
else:
    auth_ui()
