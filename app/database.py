import bcrypt
from datetime import datetime, timedelta
from app.utils import generate_api_key
from app.db_utils import get_session
from models import Admin, User, APIKey, RateLimit
from config.api_config import (
    default_expiration_time_for_api_key,
    default_request_per_minute,
    default_request_per_day,
    default_input_tokens,
    default_output_tokens,
)

salt = bcrypt.gensalt()


def get_admin(username):
    db = get_session()
    admin = db.query(Admin).filter(Admin.username == username).first()
    return admin


def add_admin(username, password):
    db = get_session()

    if db.query(Admin).filter(Admin.username == username).first():
        return False
    else:
        admin = Admin(username=username, password=password)
        db.add(admin)
        db.commit()
        return True


def add_user(name, email, phone_no, organization):
    db = get_session()
    user = User(name=name, email=email, phone_no=phone_no, organization=organization)
    db.add(user)
    db.commit()


def fetch_users():
    db = get_session()
    users = db.query(User).all()
    return users


def fetch_api_keys():
    db = get_session()
    api_keys = (
        db.query(
            User.name,
            User.email,
            APIKey.api_key,
            APIKey.key_created_date,
            APIKey.key_expiry_date,
            APIKey.status,
        )
        .join(APIKey)
        .all()
    )
    return api_keys


def add_or_update_api_key(user_id):
    db = get_session()
    new_api_key = generate_api_key()
    current_time = datetime.now()
    expire_time = current_time + timedelta(days=default_expiration_time_for_api_key)

    try:
        existing_key = db.query(APIKey).filter(APIKey.user_id == user_id).first()

        if existing_key:
            existing_key.api_key = new_api_key
            existing_key.key_created_date = current_time
            existing_key.key_expiry_date = expire_time
            existing_key.status = "active"

        else:
            api_key = APIKey(
                user_id=user_id,
                api_key=new_api_key,
                key_created_date=current_time,
                key_expiry_date=expire_time,
                status="active",
            )
            db.add(api_key)
            db.commit()
            api_key_id = api_key.id
            rate_limit = RateLimit(
                api_key_id=api_key_id,
                request_per_minute=default_request_per_minute,
                request_per_day=default_request_per_day,
                input_tokens=default_input_tokens,
                output_tokens=default_output_tokens,
            )
            db.add(rate_limit)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return new_api_key


def insert_predefined_admin():
    ADMIN_DATA = {
        "admin": {
            "password": "Password+123",
        }
    }
    for username, data in ADMIN_DATA.items():
        password_bytes = data["password"].encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        add_admin(username, hashed_password)


insert_predefined_admin()
