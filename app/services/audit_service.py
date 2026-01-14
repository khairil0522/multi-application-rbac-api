from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
from datetime import datetime

class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        *,
        user_id: int,
        action: str,
        resource: str,
        app_code: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ):
        audit = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            app_code=app_code,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow(),
        )
        self.db.add(audit)
        await self.db.commit()
