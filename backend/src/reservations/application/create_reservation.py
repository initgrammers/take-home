from ..domain.reservation import Reservation
from ..domain.reservation_repository import ReservationRepository
from src.rooms.application.room_service import RoomService


class CreateReservationUseCase:
    def __init__(self, reservation_repo: ReservationRepository, room_service: RoomService):
        self.reservation_repo = reservation_repo
        self.room_service = room_service

    def execute(self, reservation: Reservation) -> Reservation:
        # Basic validations
        if not reservation.room_id:
            raise ValueError("room_id is required")
        if not reservation.guest_email:
            raise ValueError("guest_email is required")
        if reservation.start_date > reservation.end_date:
            raise ValueError("start_date must be less than or equal to end_date")

        # Verify room exists
        if not self.room_service.exists(reservation.room_id):
            raise ValueError("room does not exist")

        created = self.reservation_repo.create(reservation)
        return created