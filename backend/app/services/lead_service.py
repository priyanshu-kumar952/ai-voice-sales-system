from app.models.lead import LeadCreate
from app.repositories.lead_repository import LeadRepository


class LeadService:
    @staticmethod
    def create_lead(lead: LeadCreate):
        saved_lead = LeadRepository.create(lead)

        return {
            "message": "Lead received",
            "lead": saved_lead,
        }