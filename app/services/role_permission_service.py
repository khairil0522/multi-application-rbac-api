from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.role_permission import RolePermission

class RolePermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assign(self, role_id: int, permission_id: int):
        # cek duplikat
        result = await self.db.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )
        if result.scalar_one_or_none():
            return False

        self.db.add(
            RolePermission(
                role_id=role_id,
                permission_id=permission_id,
            )
        )
        await self.db.commit()
        return True

    async def revoke(self, role_id: int, permission_id: int):
        result = await self.db.execute(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )
        rp = result.scalar_one_or_none()

        if not rp:
            return False

        await self.db.delete(rp)
        await self.db.commit()
        return True
