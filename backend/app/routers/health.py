from fastapi import APIRouter

from app.core.config import settings


router = APIRouter(
    prefix="",
    tags=["Health"],
)


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
    }