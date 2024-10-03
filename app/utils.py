import streamlit as st
import secrets


def hide_anchor_link():
    st.markdown(
        """
        <style>
        .stApp a:first-child {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def generate_api_key(length=20):
    return secrets.token_urlsafe(length)
