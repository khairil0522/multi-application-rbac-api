from app.core.config import settings
from app.api.v1.admin.application import router as admin_router

if settings.ENABLE_APPLICATION_ADMIN:
    from app.api.v1.admin.application import router as application_router
    admin_router.include_router(application_router)

router = admin_router