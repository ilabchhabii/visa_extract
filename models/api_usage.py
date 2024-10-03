from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from models.base import Base

class APIUsage(Base):
    __tablename__ = "api_usage"

    id = mapped_column(Integer, primary_key=True, index=True)
    api_key = mapped_column(String, nullable=False)
    input_tokens = mapped_column(Integer, nullable=False)
    output_tokens = mapped_column(Integer, nullable=False)
    cost = mapped_column(Numeric(10, 6), nullable=False,default=0.0)
    timestamp = mapped_column(DateTime(timezone=True), server_default=func.now())


