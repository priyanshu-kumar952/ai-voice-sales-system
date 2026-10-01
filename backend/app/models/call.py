from datetime import datetime

from pydantic import BaseModel


class CallCreate(BaseModel):
    call_id: str
    lead_id: int | None = None
    phone_number: str | None = None
    status: str = "started"


class CallUpdate(BaseModel):
    status: str | None = None
    ended_at: datetime | None = None
    duration_seconds: int | None = None
    transcript: str | None = None