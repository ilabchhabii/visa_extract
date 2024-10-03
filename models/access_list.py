from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship

from models.base import Base


class AccessList(Base):
    __tablename__ = "access_list"

    id = mapped_column(Integer, primary_key=True, index=True)
    task_name = mapped_column(String, nullable=False)
    URI = mapped_column(String, nullable=False)

    api_keys_access = relationship("APIKeyAccess", back_populates="access_list")
