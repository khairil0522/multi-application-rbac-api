from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        *,
        user_id: int | None,
        action: str,
        resource: str,
        app_code: str | None,
        ip_address: str | None,
        user_agent: str | None,
        status_code: int,
    ):
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            app_code=app_code,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.db.add(log)
        await self.db.commit()
