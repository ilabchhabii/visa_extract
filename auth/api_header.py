from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.api_key import APIKey
from utils.custom_exception import CustomException
from database import get_db

header_scheme = APIKeyHeader(name="x-key")


def get_client_details(
    api_key: str = Depends(header_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        db_api_key = db.query(APIKey).filter(APIKey.api_key == api_key).first()
        if db_api_key is None:
            raise credentials_exception
        return db_api_key.api_key

    except SQLAlchemyError:
        raise CustomException(
            message="An error occured getting client details for authentication"
        )


def get_client_api(
    api_key: str = Depends(header_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        db_api_key = db.query(APIKey).filter(APIKey.api_key == api_key).first()
        if db_api_key is None:
            raise credentials_exception
        return db_api_key

    except SQLAlchemyError:
        raise CustomException(
            message="An error occured getting client details for authentication"
        )
