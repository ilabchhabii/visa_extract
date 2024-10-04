import streamlit as st
from app.database import add_user, fetch_users, add_or_update_api_key, fetch_api_keys
import time
from models import APIKey, RateLimit, User, APIUsage
from app.db_utils import get_session
from sqlalchemy import func

def user_onboarding():
    st.subheader("User Onboarding")

    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "form_key" not in st.session_state:
        st.session_state.form_key = int(time.time())

    if st.session_state.submitted:
        st.session_state["name"] = ""
        st.session_state["email"] = ""
        st.session_state["phone"] = ""
        st.session_state["org"] = ""
        st.session_state.submitted = False
    with st.form("user_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", key="name")
            email = st.text_input("Email", key="email")
        with col2:
            phone_no = st.text_input("Phone Number", key="phone")
            organization = st.text_input("Organization", key="org")

        submitted = st.form_submit_button("Add User")

        if submitted:
            st.session_state.submitted = True
            db_session = get_session()
            user_exists = db_session.query(User).filter(User.email == email).first()
            if user_exists:
                st.warning("User already exists")
            else:
                add_user(name, email, phone_no, organization)
                st.success("User added successfully!")
                time.sleep(1)
                st.rerun()


def user_lists():
    db_session = get_session()
    st.subheader("User Lists")
    users = fetch_users()
    st.markdown("***")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
    with col1:
        st.markdown("<h5>Name</h5>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h5>Email</h5>", unsafe_allow_html=True)
    with col3:
        st.markdown("<h5>Phone no.</h5>", unsafe_allow_html=True)
    with col4:
        st.markdown("<h5>Organization</h5>", unsafe_allow_html=True)
    with col5:
        st.markdown("<h5>API KEY</h5>", unsafe_allow_html=True)

    st.write("***")
    for user in users:

        id, name, email, phone_no, organization = (
            user.id,
            user.name,
            user.email,
            user.phone_no,
            user.organization,
        )

        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
        with col1:
            st.write(name)
        with col2:
            st.markdown(
                f"<p style='color:yellow;'> {email} </p>", unsafe_allow_html=True
            )
        with col3:
            st.write(phone_no)
        with col4:
            st.write(organization)
        with col5:
            api_key_data = db_session.query(APIKey).filter(APIKey.user_id == id).first()

            if api_key_data:
                api_key, status = api_key_data.api_key, api_key_data.status
                if status.lower() == "inactive":
                    st.markdown(
                        "<p style='color:red;'>Inactive</p>",
                        help="API Key is inactive.",
                        unsafe_allow_html=True,
                    )

                    if st.button("Generate New API Key", key=f"generate_api_key_{id}"):
                        add_or_update_api_key(id)
                        st.success(f"New API Key generated for user {id}")
                        st.rerun()
                else:
                    st.markdown(
                        "<p style='color:green;'>Active</p>",
                        help=f"Api Key: {api_key}",
                        unsafe_allow_html=True,
                    )
            else:
                if st.button("Generate API Key", key=f"generate_api_key_{id}"):
                    add_or_update_api_key(id)
                    st.success(f"New API Key generated for user {id}")
                    st.rerun()


def toggle_api_key_status(api_key, current_status):
    db_session = get_session()
    new_status = "inactive" if current_status == "active" else "active"
    result = db_session.query(APIKey).filter(APIKey.api_key == api_key).first()
    if result:
        result.status = new_status
    else:
        st.warning("API Key not found")
    db_session.commit()


def api_key_listings():
    st.subheader("API Key Listings")
    db_session = get_session()
    api_keys = fetch_api_keys()
    if api_keys:
        st.write("***")

        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1, 1, 3, 1, 1, 1, 1, 1, 1, 1])
        with col1:
            st.markdown("<h5>Name</h5>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h5>Email</h5>", unsafe_allow_html=True)
        with col3:
            st.markdown("<h5>API Key</h5>", unsafe_allow_html=True)
        with col4:
            st.markdown("<h5>Created At</h5>", unsafe_allow_html=True)
        with col5:
            st.markdown("<h5>Expire At</h5>", unsafe_allow_html=True)
        with col6:
            st.markdown("<h5>Status</h5>", unsafe_allow_html=True)
        with col7:
            st.markdown("<h5>Input Tokens</h5>", unsafe_allow_html=True)
        with col8:
            st.markdown("<h5>Output Tokens</h5>", unsafe_allow_html=True)
        with col9:
            st.markdown("<h5>Cost ($)</h5>", unsafe_allow_html=True)
        with col10:
            st.markdown("<h5>Action</h5>", unsafe_allow_html=True)

        st.write("***")
        for i, (name, email, api_key, created_at, expire_at, status) in enumerate(
            api_keys
        ):
            usage_data = db_session.query(
                func.sum(APIUsage.input_tokens).label('total_input_tokens'),
                func.sum(APIUsage.output_tokens).label('total_output_tokens'),
                func.sum(APIUsage.cost).label('total_cost')
            ).filter(APIUsage.api_key == api_key).first()

            total_input_tokens = usage_data.total_input_tokens or 0
            total_output_tokens = usage_data.total_output_tokens or 0
            total_cost = usage_data.total_cost or 0.0

            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1, 1, 3, 1, 1, 1, 1, 1, 1, 1])
            with col1:
                st.write(name)
            with col2:
                st.markdown(f"<p style='color:yellow;'> {email} </p>", unsafe_allow_html=True)
            with col3:
                key_col, eye_col = st.columns([5, 1])
                with eye_col:
                    show_key = st.checkbox("👁️", key=f"toggle_eye_{api_key}_{i}")
                    api_key_display = api_key if show_key else "#" * 20
                with key_col:
                    st.write(api_key_display)
            with col4:
                st.markdown(f"{str(created_at).split('.')[0]}")
            with col5:
                st.markdown(f"{str(expire_at).split('.')[0]}")
            with col6:
                status_color = "green" if status.lower() == "active" else "red"
                st.markdown(f"<p style='color:{status_color};'>{status.capitalize()}</p>", unsafe_allow_html=True)
            with col7:
                st.write(f"{total_input_tokens:,}")
            with col8:
                st.write(f"{total_output_tokens:,}")
            with col9:
                st.write(f"{total_cost:.6f}")
            with col10:
                toggle_label = "Deactivate" if status == "active" else "Activate"
                if st.button(toggle_label, key=f"toggle_{api_key}_{i}"):
                    toggle_api_key_status(api_key, status)
                    time.sleep(1)
                    st.rerun()
                    


def rate_limit_settings():
    db_session = get_session()
    st.header("API Key Rate Limit Settings")
    api_key_input = st.text_input("Enter API Key")
    if api_key_input:
        api_key = (
            db_session.query(APIKey).filter(APIKey.api_key == api_key_input).first()
        )
        if api_key:
            st.success("API is valid.")
            rate_limits = (
                db_session.query(RateLimit)
                .filter(RateLimit.api_key_id == api_key.id)
                .first()
            )
            st.write("Current Rate Limit:")
            cols = st.columns(2)
            with cols[0]:
                requests_per_minute = st.number_input(
                    "Rquests per minute", value=rate_limits.request_per_minute
                )
                requests_per_day = st.number_input(
                    "Rquests per day", value=rate_limits.request_per_day
                )
            with cols[1]:
                input_tokens = st.number_input(
                    "Input Tokens", value=rate_limits.input_tokens
                )
                output_tokens = st.number_input(
                    "Output Tokens", value=rate_limits.output_tokens
                )

            if st.button("Save"):
                rate_limits.request_per_minute = requests_per_minute
                rate_limits.request_per_day = requests_per_day
                rate_limits.input_tokens = input_tokens
                rate_limits.output_tokens = output_tokens
                db_session.commit()
                st.success("Rate Limit settings saved successfully.")
                time.sleep(1)
                st.rerun()

        else:
            st.error("Invalid API key.")



def user_onboarding_page():
    st.title("Ready to Onboard user?")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["User Onboarding", "User Lists", "API Key Listings", "Rate Limit Settings"]
    )
    with tab1:
        user_onboarding()
    with tab2:
        user_lists()
    with tab3:
        api_key_listings()
    with tab4:
        rate_limit_settings()

