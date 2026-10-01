from fastapi import APIRouter

from app.models.lead import LeadCreate
from app.services.lead_service import LeadService

router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


@router.get("/health")
async def leads_health():
    return {
        "status": "healthy",
        "service": "leads",
    }


@router.post("/")
async def create_lead(lead: LeadCreate):
    return LeadService.create_lead(lead)