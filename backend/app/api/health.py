from fastapi import APIRouter
from app.providers.factory import get_railway_provider
from app.config import settings
from datetime import datetime, timezone

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("")
async def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/providers")
async def provider_health():
    provider = get_railway_provider()
    return await provider.get_provider_health()

