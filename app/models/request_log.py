from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.base import Base


class RequestLog(Base):
    __tablename__ = "tbl_request_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    method = Column(String(10), nullable=False)
    path = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    app_code = Column(String(50), nullable=True)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
