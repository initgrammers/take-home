from ..domain.reservation import Reservation
from ..domain.reservation_repository import ReservationRepository


class CreateReservationUseCase:
    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    def execute(self, reservation: Reservation) -> Reservation:
        # Basic validations similar to typical use case checks
        if not reservation.room_id:
            raise ValueError("room_id is required")
        if not reservation.guest_email:
            raise ValueError("guest_email is required")
        if reservation.start_date > reservation.end_date:
            raise ValueError("start_date must be less than or equal to end_date")

        created = self.reservation_repo.create(reservation)
        return created