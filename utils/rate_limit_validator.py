from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.api_usage import APIUsage
from utils.custom_exception import CustomException
from database import get_db
from datetime import datetime, timedelta
import pytz
from sqlalchemy import func
from models.rate_limit import RateLimit
from models.api_key import APIKey
from typing import Annotated

header_scheme = APIKeyHeader(name="x-key")


def rate_limit_validator(
    api_key: Annotated[str, Depends(header_scheme)], db: Annotated[Session, Depends(get_db)]
):
    
    
    try:
        rate_limit = db.query(RateLimit).join(APIKey).filter(
            APIKey.api_key == api_key
            ).first()
        
        if not rate_limit:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        
        time_now = datetime.now(pytz.utc).replace(microsecond=0, tzinfo=None)
        
        num_of_requests_per_minute = db.query(APIUsage).filter(
            APIUsage.api_key == api_key,
            APIUsage.timestamp >= time_now - timedelta(minutes=1),
        ).count()

        num_of_requests_per_day = db.query(APIUsage).filter(
            APIUsage.api_key == api_key,
            APIUsage.timestamp >= time_now - timedelta(days=1),
        ).count()

        total_input_tokens = (
            db.query(func.sum(APIUsage.input_tokens))
            .filter(
                APIUsage.api_key == api_key,
                APIUsage.timestamp >= time_now - timedelta(days=1),
            )
            .scalar()
        ) or 0

        total_output_tokens = (
            db.query(func.sum(APIUsage.output_tokens))
            .filter(
                APIUsage.api_key == api_key,
                APIUsage.timestamp >= time_now - timedelta(days=1),
            )
            .scalar()
        ) or 0

        if (
            num_of_requests_per_day >= rate_limit.request_per_day
            or total_input_tokens >= rate_limit.input_tokens
            or total_output_tokens >= rate_limit.output_tokens
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You have exceeded the daily usage limit.",
            )
        else:
            if num_of_requests_per_minute >= rate_limit.request_per_minute:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many Requests. Please wait for a minute.",
                )
    except SQLAlchemyError:
        raise CustomException(message="An error occured getting api usage details.")
