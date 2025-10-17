from ..domain.room_repository import RoomRepository

class RoomService:
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo

    def exists(self, room_id: str) -> bool:
        return self.room_repo.get_by_id(room_id) is not None