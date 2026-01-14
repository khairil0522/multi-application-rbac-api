import json
from app.core.redis import redis_client

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.application import Application
from app.models.user_application import UserApplication
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.core.security import verify_password, create_access_token, hash_password
from app.core.permission_cache import perm_cache_key


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_user_permissions(self, user_id: int, app_code: str):
        stmt = (
            select(Permission.code)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .join(Application, Application.id == RolePermission.application_id)
            .where(
                UserRole.user_id == user_id,
                RolePermission.application_id == UserRole.application_id
            )
            .distinct()
        )

        result = await self.db.execute(stmt)
        return [row[0] for row in result.all()]
    

    # ========= LOGIN =========
    async def login(self, email: str, password: str, app_code: str):
        # 1️⃣ Cek aplikasi
        result = await self.db.execute(
            select(Application).where(Application.code == app_code)
        )
        app = result.scalar_one_or_none()
        if not app:
            raise HTTPException(400, "Invalid application")

        # 2️⃣ Cek user
        result = await self.db.execute(
            select(User).where(
                User.email == email,
                User.status == "ACTIVE",
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(401, "Invalid email or password")

        # 3️⃣ Verify password
        if not verify_password(password, user.password_hash):
            raise HTTPException(401, "Invalid email or password")

        # 4️⃣ Cek user terdaftar di app?
        result = await self.db.execute(
            select(UserApplication).where(
                UserApplication.user_id == user.id,
                UserApplication.application_id == app.id,
                UserApplication.status == "ACTIVE",
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                403,
                "User is not registered in this application",
            )

        # 5️⃣ Ambil role user di app ini
        result = await self.db.execute(
            select(Role.code)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(
                UserRole.user_id == user.id,
                UserRole.application_id == app.id,
            )
        )
        roles = [row[0] for row in result.all()]

        permissions = await self._get_user_permissions(user.id, app_code)

        # 6️⃣ Generate JWT (TERIKAT APP)
        token = create_access_token(
            subject=str(user.id),
            roles=roles,
            app_code=app.code,
        )

        # Redis
        redis_client.set(
            perm_cache_key(user.id, app_code),
            json.dumps(permissions),
            ex=3600
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "roles": roles,
                "app": app.code,
            },
        }
    
        audit = AuditService(self.db)

        try:
            # normal login logic
            ...
            await audit.log(
                user_id=user.id,
                action="LOGIN_SUCCESS",
                resource="auth/login",
                app_code=app_code,
                request=request,
            )

            return result

        except HTTPException:
            await audit.log(
                user_id=None,
                action="LOGIN_FAILED",
                resource="auth/login",
                app_code=app_code,
                request=request,
            )
            raise    

    # ========= REGISTER =========
    async def register(self, payload):
        # 1. Ambil application
        result = await self.db.execute(
            select(Application).where(Application.code == payload.app_code)
        )
        app = result.scalar_one_or_none()

        if not app:
            raise HTTPException(400, "Invalid application")

        # 2. Cek user global
        result = await self.db.execute(
            select(User).where(User.email == payload.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                email=payload.email,
                full_name=payload.full_name,
                password_hash=hash_password(payload.password),
                status="ACTIVE",
            )
            self.db.add(user)
            await self.db.flush()  # ⬅️ dapat user.id tanpa commit

        # 3. Cek user sudah terdaftar di app?
        result = await self.db.execute(
            select(UserApplication).where(
                UserApplication.user_id == user.id,
                UserApplication.application_id == app.id,
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="User already registered in this application",
            )

        # 4. Register user ke app
        user_app = UserApplication(
            user_id=user.id,
            application_id=app.id,
            status="ACTIVE",
        )
        self.db.add(user_app)

        # 5. Assign default role USER
        result = await self.db.execute(
            select(Role).where(Role.code == "USER")
        )
        role = result.scalar_one()

        self.db.add(
            UserRole(
                user_id=user.id,
                role_id=role.id,
                application_id=app.id,  # ⬅️ penting untuk multi-app
            )
        )

        await self.db.commit()

        return user    

    # ========= PRIVATE HELPERS =========
    async def _get_user_by_email(self, email: str):
        stmt = select(User).where(
            User.email == email,
            User.status == "ACTIVE",
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_user_roles(self, user_id: int):
        stmt = (
            select(Role.code)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return [row[0] for row in result.all()]
