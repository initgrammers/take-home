from abc import ABC, abstractmethod
from typing import Sequence, Optional
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