from typing import Sequence, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..domain.reservation import Reservation
from ..domain.reservation_repository import ReservationRepository
from .reservation_model_psql import ReservationModel

class ReservationRepositoryPsql(ReservationRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[Reservation]:
        rows = self.session.query(ReservationModel).all()
        return [
            Reservation(
                id=row.id,
                room_id=row.room_id,
                guest_email=row.guest_email,
                start_date=row.start_date,
                end_date=row.end_date,
                status=row.status,
            )
            for row in rows
        ]

    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        row = self.session.get(ReservationModel, reservation_id)
        if not row:
            return None
        return Reservation(
            id=row.id,
            room_id=row.room_id,
            guest_email=row.guest_email,
            start_date=row.start_date,
            end_date=row.end_date,
            status=row.status,
        )

    def create(self, reservation: Reservation) -> Reservation:
        row = ReservationModel(
            id=reservation.id,
            room_id=reservation.room_id,
            guest_email=reservation.guest_email,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            status=reservation.status,
        )
        self.session.add(row)
        try:
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Reservation with this id already exists")
        return Reservation(
            id=row.id,
            room_id=row.room_id,
            guest_email=row.guest_email,
            start_date=row.start_date,
            end_date=row.end_date,
            status=row.status,
        )