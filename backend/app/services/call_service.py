from app.models.call import CallCreate, CallUpdate
from app.repositories.call_repository import CallRepository


class CallService:

    @staticmethod
    def create_call(call: CallCreate):
        return CallRepository.create(call)

    @staticmethod
    def update_call(call_id: str, call: CallUpdate):
        return CallRepository.update(call_id, call)