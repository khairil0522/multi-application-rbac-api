from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.application import Application

class ApplicationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload):
        exists = await self.db.scalar(
            select(Application).where(Application.code == payload.code)
        )
        if exists:
            raise HTTPException(409, "Application code already exists")

        app = Application(
            code=payload.code,
            name=payload.name,
            is_active=True,
        )
        self.db.add(app)
        await self.db.commit()
        await self.db.refresh(app)
        return app

    async def list(self):
        result = await self.db.execute(select(Application))
        return result.scalars().all()

    async def update(self, app_id: int, payload):
        app = await self.db.get(Application, app_id)
        if not app:
            raise HTTPException(404, "Application not found")

        if payload.name is not None:
            app.name = payload.name

        await self.db.commit()
        await self.db.refresh(app)
        return app

    async def set_status(self, app_id: int, is_active: bool):
        app = await self.db.get(Application, app_id)
        if not app:
            raise HTTPException(404, "Application not found")

        app.is_active = is_active
        await self.db.commit()
