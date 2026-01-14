# app/models/role.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.base import Base

class Role(Base):
    __tablename__ = "tbl_role"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("tbl_application.id"), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(100))
    description = Column(String(255))
