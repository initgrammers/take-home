from ..domain.reservation import Reservation
from ..domain.reservation_repository import ReservationRepository

class CancelReservationUseCase:
    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    def execute(self, reservation_id: str) -> Reservation:
        if not reservation_id:
            raise ValueError("reservation_id is required")
        updated = self.reservation_repo.cancel(reservation_id)
        return updated