from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from models.base import Base


class Admin(Base):
    __tablename__ = "admin"

    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, nullable=False)
    password = mapped_column(String, nullable=False)