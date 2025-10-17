from datetime import date
from typing import List, Dict, Any
from ..domain.room import Room

from ..domain.room_repository import RoomRepository
#from app.application.services.availability import AvailabilityService

class ListRoomsUseCase:
    # def __init__(self, room_repo: RoomRepository, availability: AvailabilityService):
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo
       #self.availability = availability

    def execute(self) -> List[Room]:
        rooms = self.room_repo.get_all()
        today = date.today()
        result = []
        # for r in rooms:
        #     available_today = self.availability.is_available(r.id, today, today)
        #     result.append({
        #         "id": r.id,
        #         "number": r.number,
        #         "type": r.type,
        #         "capacity": r.capacity,
        #         "price_per_night": float(r.price_per_night),
        #         "available_today": available_today,
        #     })
        return rooms