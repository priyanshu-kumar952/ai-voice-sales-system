from pydantic import BaseModel


class CheckInventoryRequest(BaseModel):
    location: str | None = None
    property_type: str | None = None
    max_budget: int | None = None


class TransferCallRequest(BaseModel):
    reason: str
    phone_number: str | None = None