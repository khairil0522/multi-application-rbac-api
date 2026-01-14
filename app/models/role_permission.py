# app/models/role_permission.py
from sqlalchemy import Column, Integer, ForeignKey
from app.core.base import Base

class RolePermission(Base):
    __tablename__ = "tbl_role_permission"

    role_id = Column(Integer, ForeignKey("tbl_role.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("tbl_permission.id"), primary_key=True)
