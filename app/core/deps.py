import json
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_token
from app.core.redis import redis_client
from app.models.application import Application
from app.models.role_permission import RolePermission
from app.models.permission import Permission
from app.models.user import User
from app.models.user_role import UserRole

security = HTTPBearer()

def require_permission(permission_code: str):
    async def checker(
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        user_id = current_user["id"]
        app_code = current_user["app_code"]

        cache_key = f"perm:{user_id}:{app_code}"

        # 1️⃣ Redis HIT
        try:
            cached = redis_client.get(cache_key)
            if cached:
                permissions = json.loads(cached)
                if permission_code not in permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Permission denied",
                    )
                return True
        except Exception:
            # Redis down → fallback DB
            pass

        # 2️⃣ Redis MISS → DB
        stmt = (
            select(Permission.code)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .join(Application, Application.id == RolePermission.application_id)
            .where(
                UserRole.user_id == user_id,
                Application.code == app_code,
            )
            .distinct()
        )

        result = await db.execute(stmt)
        permissions = [row[0] for row in result.all()]

        # 3️⃣ Save to Redis
        try:
            redis_client.set(
                cache_key,
                json.dumps(permissions),
                ex=3600,
            )
        except Exception:
            pass

        if permission_code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return True

    return checker

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials

    payload = decode_token(token)

    user_id = payload.get("sub")
    app_code = payload.get("app")

    if not user_id or not app_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await db.scalar(
        select(User).where(
            User.id == int(user_id),
            User.status == "ACTIVE",
        )
    )

    if not user:
        raise HTTPException(401, "User not found")

    return {
        "id": user.id,
        "email": user.email,
        "roles": payload.get("roles", []),
        "app_code": app_code,
    }