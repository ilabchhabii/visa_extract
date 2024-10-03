from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from models.base import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    phone_no = mapped_column(String, nullable=False)
    organization = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True)
    api_keys = relationship("APIKey", back_populates="user")
