from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
)
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/admin/applications",
    tags=["Admin - Application"],
    dependencies=[Depends(require_permission("APP_MANAGE"))],
)

#Create
@router.post("", response_model=ApplicationResponse)
async def create_application(
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)
    return await service.create(payload)

#Read
@router.post("", response_model=ApplicationResponse)
async def create_application(
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)
    return await service.create(payload)

#Update
@router.get("", response_model=list[ApplicationResponse])
async def list_applications(
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)
    return await service.list()

#Delete
@router.patch("/{app_id}/status")
async def set_application_status(
    app_id: int,
    is_active: bool,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)
    await service.set_status(app_id, is_active)
    return {"message": "Application status updated"}
