from app.models.inventory import InventorySearch
from app.repositories.inventory_repository import InventoryRepository


class InventoryService:
    @staticmethod
    def search_inventory(search: InventorySearch):
        return InventoryRepository.search(
            location=search.location,
            property_type=search.property_type,
            max_budget=search.max_budget,
        )