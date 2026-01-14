from fastapi import FastAPI
from app.api.v1 import auth, admin
from app.core.config import settings

from app.middleware.audit import AuditMiddleware

app = FastAPI(
    title="MultiApp API",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth.router)
app.include_router(admin.router)
app.add_middleware(AuditMiddleware)
