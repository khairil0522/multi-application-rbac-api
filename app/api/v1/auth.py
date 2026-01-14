from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService
from app.core.database import get_db
from app.core.deps import get_current_user, require_permission

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    audit = AuditService(db)
    result = await service.login(
        payload.email, 
        payload.password,
        payload.app_code,
    )

    return {
        "status": {"code": 200, "message": "Login successful"},
        "data": result,
    }

@router.post("/register")
async def register(
    payload: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    audit = AuditService(db)

    user = await service.register(payload)

    return {
        "status": {"code": 201, "message": "User registered"},
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
        },
    }

@router.get("/validate")
async def validate_token(
    current_user=Depends(get_current_user),
):
    return {
        "status": {"code": 200, "message": "Token valid"},
        "data": current_user,
    }

@router.get("/me")
async def me(current_user = Depends(get_current_user)):
    return {
        "status": {"code": 200, "message": "Success"},
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
        },
    }