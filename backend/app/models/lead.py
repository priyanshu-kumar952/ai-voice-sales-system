from pydantic import BaseModel


class Lead(BaseModel):
    name: str
    phone: str
    budget: int | None = None
    preferred_location: str | None = None
    property_type: str | None = None


class LeadCreate(BaseModel):
    name: str
    phone: str
    budget: int | None = None
    preferred_location: str | None = None
    property_type: str | None = None