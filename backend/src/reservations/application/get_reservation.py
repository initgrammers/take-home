from ..domain.reservation import Reservation
from ..domain.reservation_repository import ReservationRepository


class GetReservationUseCase:
    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    def execute(self, reservation_id: str) -> Reservation:
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("reservation not found")
        return reservation