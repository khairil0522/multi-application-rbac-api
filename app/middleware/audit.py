from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.audit import AuditService
from app.core.security import decode_token_safely  # kita bikin helper kecil

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # ❗ skip docs & health
        if request.url.path.startswith(("/docs", "/openapi", "/health")):
            return response

        user_id = None
        app_code = None

        # ambil token kalau ada
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.replace("Bearer ", "")
            payload = decode_token_safely(token)
            if payload:
                user_id = payload.get("id")
                app_code = payload.get("app_code")

        async with AsyncSessionLocal() as db:
            audit = AuditService(db)
            await audit.log(
                user_id=user_id,
                action=f"{request.method}",
                resource=request.url.path,
                app_code=app_code,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                status_code=response.status_code,
            )

        return response
