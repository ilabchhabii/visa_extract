from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from models.base import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    api_key = mapped_column(String, unique=True, nullable=False)
    key_created_date = mapped_column(DateTime(timezone=True), server_default=func.now())
    key_expiry_date = mapped_column(DateTime(timezone=True), nullable=False)
    status = mapped_column(String, nullable=False, default="active")

    user = relationship("User", back_populates="api_keys")
    api_keys_access = relationship("APIKeyAccess", back_populates="api_key")
    rate_limit = relationship("RateLimit", back_populates="api_key")
