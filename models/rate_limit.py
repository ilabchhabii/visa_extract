from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from models.base import Base


class RateLimit(Base):
    __tablename__ = "rate_limit"

    id = mapped_column(Integer, primary_key=True, index=True)
    api_key_id = mapped_column(Integer, ForeignKey("api_keys.id"), nullable=False)
    request_per_minute = mapped_column(Integer, nullable=False, default=2)
    request_per_day = mapped_column(Integer, nullable=False, default=20)
    input_tokens = mapped_column(Integer, nullable=False, default=1000000)
    output_tokens = mapped_column(Integer, nullable=False, default=1000000)
    api_key = relationship("APIKey", back_populates="rate_limit")
