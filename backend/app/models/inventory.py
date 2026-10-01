from pydantic import BaseModel


class InventorySearch(BaseModel):
    location: str | None = None
    property_type: str | None = None
    max_budget: int | None = None