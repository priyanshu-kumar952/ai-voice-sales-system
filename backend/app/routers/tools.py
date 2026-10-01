from fastapi import APIRouter, Depends

from app.core.rate_limit import rate_limit
from app.models.tools import (
    CheckInventoryRequest,
    TransferCallRequest,
)
from app.services.inventory_service import InventoryService


router = APIRouter(
    prefix="/tools",
    tags=["Agent Tools"],
    dependencies=[Depends(rate_limit)],
)


@router.post("/check_inventory")
async def check_inventory(request: CheckInventoryRequest):
    results = InventoryService.search_inventory(request)

    return {
        "success": True,
        "results": results,
    }


@router.post("/transfer_call")
async def transfer_call(request: TransferCallRequest):
    return {
        "success": True,
        "action": "transfer_call",
        "reason": request.reason,
        "phone_number": request.phone_number,
        "message": "Call transfer requested",
    }


