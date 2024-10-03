from app.db_utils import get_session
from sqlalchemy.orm import Session
from models.user import User
from fastapi import Depends


async def get_current_user(user_id: int, db: Session = Depends(get_session)):
    return db.query(User).filter(User.id == id).first()
