
from typing import Sequence, Optional
from decimal import Decimal
from sqlalchemy.orm import Session

from ..domain.room import Room
from ..domain.room_repository import RoomRepository
from .room_model_psql import RoomModel

class RoomRepositoryPsql(RoomRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[Room]:
        rows = self.session.query(RoomModel).all()
        return [
            Room(
                id=row.id,
                name=row.name,
                price_per_night=Decimal(str(row.price_per_night)),
            )
            for row in rows
        ]

    def get_by_id(self, room_id: str) -> Optional[Room]:
        row = self.session.get(RoomModel, room_id)
        if not row:
            return None
        return Room(
            id=row.id,
            name=row.name,
            price_per_night=Decimal(str(row.price_per_night)),
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