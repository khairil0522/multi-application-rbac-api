from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.base import Base

class UserApplication(Base):
    __tablename__ = "tbl_user_application"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("tbl_user.id", ondelete="CASCADE"), nullable=False)
    application_id = Column(Integer, ForeignKey("tbl_application.id", ondelete="CASCADE"), nullable=False)

    status = Column(String(20), default="ACTIVE", nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "application_id", name="uq_user_application"),
    )

    user = relationship("User", backref="applications")
    application = relationship("Application", backref="users")