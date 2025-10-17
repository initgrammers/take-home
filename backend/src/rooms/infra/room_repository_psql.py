
from typing import Sequence, Optional
from decimal import Decimal
from sqlalchemy.orm import Session

from ..domain.room import Room, ReservationRange
from ..domain.room_repository import RoomRepository
from .room_model_psql import RoomModel
from src.reservations.infra.reservation_model_psql import ReservationModel

class RoomRepositoryPsql(RoomRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[Room]:
        rows = self.session.query(RoomModel).all()
        rooms: list[Room] = []
        for row in rows:
            res_rows = (
                self.session.query(ReservationModel)
                .filter(
                    ReservationModel.room_id == row.id,
                    ReservationModel.status == "active",
                )
                .all()
            )
            reservation_ranges = [
                ReservationRange(start_date=r.start_date, end_date=r.end_date)
                for r in res_rows
            ]
            rooms.append(
                Room(
                    id=row.id,
                    name=row.name,
                    price_per_night=Decimal(str(row.price_per_night)),
                    reservation_ranges=reservation_ranges,
                )
            )
        return rooms

    def get_by_id(self, room_id: str) -> Optional[Room]:
        row = self.session.get(RoomModel, room_id)
        if not row:
            return None
        res_rows = (
            self.session.query(ReservationModel)
            .filter(
                ReservationModel.room_id == room_id,
                ReservationModel.status == "active",
            )
            .all()
        )
        reservation_ranges = [
            ReservationRange(start_date=r.start_date, end_date=r.end_date)
            for r in res_rows
        ]
        return Room(
            id=row.id,
            name=row.name,
            price_per_night=Decimal(str(row.price_per_night)),
            reservation_ranges=reservation_ranges,
        )

    def create(self, room: Room) -> Room:
        row = RoomModel(
            id=room.id,
            name=room.name,
            price_per_night=room.price_per_night,
        )
        self.session.add(row)
        self.session.flush()
        room.id = row.id
        return room