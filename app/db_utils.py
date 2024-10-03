from database import get_db
def get_session():
    return next(get_db())
