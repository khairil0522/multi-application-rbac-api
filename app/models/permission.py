# app/models/permission.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.base import Base

class Permission(Base):
    __tablename__ = "tbl_permission"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("tbl_application.id"), nullable=False)
    code = Column(String(100), nullable=False)
    description = Column(String(255))
