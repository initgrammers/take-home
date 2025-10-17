from abc import ABC, abstractmethod
from typing import Sequence, Optional
from datetime import date
from .reservation import Reservation

class ReservationRepository(ABC):
    @abstractmethod
    def get_all(self) -> Sequence[Reservation]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        raise NotImplementedError

    @abstractmethod
    def create(self, reservation: Reservation) -> Reservation:
        raise NotImplementedError

    @abstractmethod
    def has_overlap(self, room_id: str, start_date: date, end_date: date) -> bool:
        """Return True if there is any ACTIVE reservation overlapping the given range for the room."""
        raise NotImplementedError