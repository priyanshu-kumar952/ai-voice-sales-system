from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import pool
from app.routers.health import router as health_router
from app.routers.leads import router as leads_router
from app.routers.inventory import router as inventory_router
from app.routers.tools import router as tools_router
from app.routers.calls import router as calls_router
from app.routers.webhooks import router as webhooks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()

    yield

    pool.close()


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Voice AI Sales and Lead Qualification System",
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"{settings.app_name} API is running",
        "version": settings.app_version,
    }


app.include_router(health_router)
app.include_router(leads_router)
app.include_router(inventory_router)
app.include_router(tools_router)
app.include_router(calls_router)
app.include_router(webhooks_router)