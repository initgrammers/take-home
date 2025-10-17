from abc import ABC, abstractmethod
from typing import Sequence, Optional
from .room import Room

class RoomRepository(ABC):
    @abstractmethod
    def get_all(self) -> Sequence[Room]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, room_id: str) -> Optional[Room]:
        raise NotImplementedError

    @abstractmethod
    def create(self, room: Room) -> Room:
        raise NotImplementedError
        