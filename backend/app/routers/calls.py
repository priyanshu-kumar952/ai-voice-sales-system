from fastapi import APIRouter

from app.models.call import CallCreate, CallUpdate
from app.services.call_service import CallService


router = APIRouter(
    prefix="/calls",
    tags=["Calls"],
)


@router.post("/")
async def create_call(call: CallCreate):
    return {
        "success": True,
        "call": CallService.create_call(call),
    }


@router.patch("/{call_id}")
async def update_call(
    call_id: str,
    call: CallUpdate,
):
    updated_call = CallService.update_call(call_id, call)

    if updated_call is None:
        return {
            "success": False,
            "message": "Call not found",
        }

    return {
        "success": True,
        "call": updated_call,
    }