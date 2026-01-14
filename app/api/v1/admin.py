from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_permission, get_current_user
from app.schemas.role_permission import AssignPermissionRequest
from app.services.role_permission_service import RolePermissionService
from app.schemas.admin import AssignRoleRequest
from app.services.admin_service import AdminService, AuditService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_permission("ROLE_MANAGE"))],
)

## Roles and Permissions
@router.post("/roles/{role_id}/permissions")
async def assign_permission(
    role_id: int,
    payload: AssignPermissionRequest,
    db: AsyncSession = Depends(get_db),
):
    service = RolePermissionService(db)
    ok = await service.assign(role_id, payload.permission_id)

    if not ok:
        raise HTTPException(400, "Permission already assigned")

    return {
        "status": {"code": 200, "message": "Permission assigned"},
    }


@router.delete("/roles/{role_id}/permissions/{permission_id}")
async def revoke_permission(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = RolePermissionService(db)
    ok = await service.revoke(role_id, permission_id)

    if not ok:
        raise HTTPException(404, "Permission not found")

    return {
        "status": {"code": 200, "message": "Permission revoked"},
    }

## Users Roles
@router.post(
    "/users/{user_id}/roles",
    dependencies=[Depends(require_permission("ROLE_ASSIGN"))],
)
async def assign_role(
    user_id: int,
    payload: AssignRoleRequest,
    request: Request,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AdminService(db)
    audit = AuditService(db)

    await service.assign_role_to_user(
        user_id=user_id,
        role_code=payload.role_code,
        app_code=payload.app_code,
    )

    return {
        "status": {"code": 200, "message": "Role assigned"},
    }

@router.delete(
    "/users/{user_id}/roles/{role_code}",
    dependencies=[Depends(require_permission("ROLE_ASSIGN"))],
)
async def remove_role(
    user_id: int,
    role_code: str,
    request: Request,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AdminService(db)
    audit = AuditService(db)

    await service.remove_role_from_user(
        user_id=user_id,
        role_code=role_code,
    )

    return {"status": {"code": 200, "message": "Role removed"}}


## Permissions
@router.get(
    "/roles/{role_id}/permissions",
    dependencies=[Depends(require_permission("ADMIN"))],
)
async def list_role_permissions(
    role_id: int,
    app_code: str,
    db: AsyncSession = Depends(get_db),
):
    service = AdminService(db)
    permissions = await service.list_permissions_by_role(role_id, app_code)
    return {"permissions": permissions}

@router.post(
    "/roles/{role_id}/permissions",
    dependencies=[Depends(require_permission("PERMISSION_ASSIGN"))],
)
async def assign_permission_to_role(
    role_id: int,
    payload: AssignPermissionRequest,
    request: Request,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AdminService(db)
    audit = AuditService(db)

    await service.assign_permission_to_role(
        role_id=role_id,
        permission_code=payload.permission_code,
        app_code=payload.app_code,
    )

    return {
        "status": {"code": 200, "message": "Permission assigned"},
    }


