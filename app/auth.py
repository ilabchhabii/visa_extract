import streamlit as st
from app.database import get_admin
import bcrypt
import time


def authenticate(username, password):

    user = get_admin(username)
    if user and user.password:
        if bcrypt.checkpw(password.encode("utf-8"), user.password):
            return user.username
    return None


def login():
    st.sidebar.title("Login")
    st.session_state.password = ""
    username = st.sidebar.text_input("Username").lower()
    password = st.sidebar.text_input(
        "Password", type="password", autocomplete="current-password"
    )
    submit_button = st.sidebar.button("Login")

    def attempt_login():
        user_type = authenticate(username, password)
        if user_type:
            st.session_state.user = {"username": username, "type": user_type}
            st.sidebar.success("Login Successful.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")
            st.session_state.password = ""

    if submit_button:
        attempt_login()
    if "password" in st.session_state and st.session_state.password != password:
        attempt_login()
    st.session_state.password = password


def logout():
    st.session_state.user = None
    st.session_state.clear()
    st.success("Logged out successfully")
    st.rerun()
