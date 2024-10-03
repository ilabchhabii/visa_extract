from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from models.base import Base


class APIKeyAccess(Base):
    __tablename__ = "api_keys_access"

    id = mapped_column(Integer, primary_key=True, index=True)
    api_key_id = mapped_column(Integer, ForeignKey("api_keys.id"), nullable=False)
    access_list_id = mapped_column(
        Integer, ForeignKey("access_list.id"), nullable=False
    )

    api_key = relationship("APIKey", back_populates="api_keys_access")
    access_list = relationship("AccessList", back_populates="api_keys_access")
