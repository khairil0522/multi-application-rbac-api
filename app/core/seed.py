import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.application import Application
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.permission import Permission
from app.models.role_permission import RolePermission

async def seed_application(db):
    app = await db.scalar(
        select(Application).where(Application.code == "DEFAULT_APP")
    )
    if not app:
        app = Application(
            code="DEFAULT_APP",
            name="Global App",
            description="Default application",
            is_active=True,
        )
        db.add(app)
        await db.flush()
    return app

async def seed_roles(db):
    roles = [
        ("SUPER_ADMIN", "Super Administrator"),
        ("ADMIN", "Administrator"),
        ("USER", "User"),
    ]

    result = await db.execute(select(Role))
    existing = {r.code for r in result.scalars()}

    for code, name in roles:
        if code not in existing:
            db.add(Role(code=code, name=name))

    await db.flush()


async def seed_permissions(db):
    permissions = [
        ("APP_MANAGE", "Manage Applications"),
        ("USER_CREATE", "Create User"),
        ("USER_DEACTIVATE", "Deactivate User"),
        ("ROLE_ASSIGN", "Assign Role"),
    ]

    result = await db.execute(select(Permission))
    existing = {p.code for p in result.scalars()}

    for code, name in permissions:
        if code not in existing:
            db.add(
                Permission(
                    code=code,
                    name=name,
                    description=name,
                )
            )

    await db.flush()

async def seed_super_admin_permissions(db, app):
    super_admin = await db.scalar(
        select(Role).where(Role.code == "SUPER_ADMIN")
    )

    perms = await db.execute(select(Permission))
    permissions = perms.scalars().all()

    for perm in permissions:
        exists = await db.scalar(
            select(RolePermission).where(
                RolePermission.role_id == super_admin.id,
                RolePermission.permission_id == perm.id,
                RolePermission.application_id == app.id,
            )
        )
        if not exists:
            db.add(
                RolePermission(
                    role_id=super_admin.id,
                    permission_id=perm.id,
                    application_id=app.id,
                )
            )

    await db.flush()

async def seed_admin_user(db, app):
    user = await db.scalar(
        select(User).where(User.email == "admin@local.dev")
    )
    if not user:
        user = User(
            email="admin@local.dev",
            full_name="System Admin",
            password_hash=hash_password("admin123"),
            status="ACTIVE",
        )
        db.add(user)
        await db.flush()

    admin_role = await db.scalar(
        select(Role).where(Role.code == "SUPER_ADMIN")
    )

    exists = await db.scalar(
        select(UserRole).where(
            UserRole.user_id == user.id,
            UserRole.role_id == admin_role.id,
            UserRole.application_id == app.id,
        )
    )

    if not exists:
        db.add(
            UserRole(
                user_id=user.id,
                role_id=admin_role.id,
                application_id=app.id,
            )
        )

    await db.flush()

async def seed():
    async with AsyncSessionLocal() as db:
        app = await seed_application(db)
        await seed_roles(db)
        await seed_permissions(db)
        await seed_super_admin_permissions(db, app)
        await seed_admin_user(db, app)

        await db.commit()
        print("✅ Seed completed")

if __name__ == "__main__":
    asyncio.run(seed())
