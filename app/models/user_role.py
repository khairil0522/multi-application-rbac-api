# app/models/user_role.py
from sqlalchemy import Column, Integer, ForeignKey
from app.core.base import Base

class UserRole(Base):
    __tablename__ = "tbl_user_role"

    user_id = Column(Integer, ForeignKey("tbl_user.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("tbl_role.id"), primary_key=True)
