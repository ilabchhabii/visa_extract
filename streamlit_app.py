import streamlit as st
from app.utils import hide_anchor_link
from app.auth import login, logout
from app.user_onboarding_page import user_onboarding_page

st.set_page_config(layout="wide", page_title="API Key Management")


def main():
    hide_anchor_link()
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        st.title("Hello, How can I help you today?")

        login()
    else:
        st.sidebar.title("User Actions")
        if st.sidebar.button("Logout", key="logout1"):
            logout()

        user_onboarding_page()


if __name__ == "__main__":
    main()
