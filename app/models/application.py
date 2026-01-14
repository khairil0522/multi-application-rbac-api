# app/models/application.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.base import Base

class Application(Base):
    __tablename__ = "tbl_application"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
