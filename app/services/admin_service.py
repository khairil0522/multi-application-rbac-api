from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Role, UserRole, Application, RolePermission, Permission
from app.core.redis import redis_client
from app.core.permission_cache import invalidate_user_app_permission, invalidate_user_all_permissions
from app.core.audit import write_audit_log


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assign_role_to_user(
        self,
        *,
        actor_id: int,
        target_user_id: int,
        role_code: str,
        app_code: str,
    ):
        app = await self.db.scalar(
            select(Application).where(Application.code == app_code)
        )
        if not app:
            raise ValueError("Application not found")

        role = await self.db.scalar(
            select(Role).where(Role.code == role_code)
        )
        if not role:
            raise ValueError("Role not found")

        exists = await self.db.scalar(
            select(UserRole).where(
                UserRole.user_id == target_user_id,
                UserRole.role_id == role.id,
                UserRole.application_id == app.id,
            )
        )
        if exists:
            return exists

        user_role = UserRole(
            user_id=target_user_id,
            role_id=role.id,
            application_id=app.id,
        )

        self.db.add(user_role)
        await self.db.commit()

        # 🔥 invalidate redis
        invalidate_user_all_permissions(target_user_id)

        # 🔥 audit
        await self.audit.log(
            user_id=actor_id,
            action="ASSIGN_ROLE",
            resource=f"user:{target_user_id}",
            app_code=app_code,
            metadata={"role": role_code},
        )

        return user_role

async def assign_permission_to_role(
    self,
    *,
    actor_id: int,
    role_id: int,
    permission_code: str,
    app_code: str,
):
    # 1️⃣ resolve application
    app = await self.db.scalar(
        select(Application).where(Application.code == app_code)
    )
    if not app:
        raise ValueError("Application not found")

    # 2️⃣ resolve permission
    permission = await self.db.scalar(
        select(Permission).where(Permission.code == permission_code)
    )
    if not permission:
        raise ValueError("Permission not found")

    # 3️⃣ cek existing mapping
    exists = await self.db.scalar(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission.id,
            RolePermission.application_id == app.id,
        )
    )
    if exists:
        return exists

    # 4️⃣ create mapping
    rp = RolePermission(
        role_id=role_id,
        permission_id=permission.id,
        application_id=app.id,
    )
    self.db.add(rp)
    await self.db.commit()

    # 5️⃣ invalidate cache (only affected users)
    result = await self.db.execute(
        select(UserRole.user_id).where(
            UserRole.role_id == role_id,
            UserRole.application_id == app.id,
        )
    )

    for (user_id,) in result.all():
        invalidate_user_app_permission(user_id, app_code)

    # 6️⃣ audit
    await write_audit_log(
        self.db,
        user_id=actor_id,
        action="ASSIGN_PERMISSION",
        resource=f"role:{role_id}",
        app_code=app_code,
        ip_address=None,
        user_agent=None,
    )

    return rp
