# app/models/audit_log.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.base import Base

class AuditLog(Base):
    __tablename__ = "tbl_audit_log"

    id = Column(Integer, primary_key=True)

    # actor & scope
    user_id = Column(Integer, nullable=True)
    app_code = Column(String(50), nullable=True)

    # business audit (sudah ada)
    action = Column(String(50), nullable=False)
    resource = Column(String(100), nullable=True)

    # technical audit (baru)
    method = Column(String(10), nullable=True)
    path = Column(String(255), nullable=True)
    status_code = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)

    # client info
    ip_address = Column(String(50))
    user_agent = Column(Text)

    # extensibility
    extra = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())