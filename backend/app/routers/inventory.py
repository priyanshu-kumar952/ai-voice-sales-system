from fastapi import APIRouter

from app.models.inventory import InventorySearch
from app.services.inventory_service import InventoryService


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post("/search")
async def search_inventory(search: InventorySearch):
    return {
        "inventory": InventoryService.search_inventory(search),
    }