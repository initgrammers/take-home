from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.schemas import RoomOut, ReservationRangeOut
from src.rooms.application.list_room import ListRoomsUseCase
from src.rooms.infra.room_repository_psql import RoomRepositoryPsql
from src.shared.infra.db import get_session

router = APIRouter()

@router.get("/rooms", response_model=List[RoomOut])
def list_rooms(session: Session = Depends(get_session)):
    usecase = ListRoomsUseCase(RoomRepositoryPsql(session))
    rooms = usecase.execute()
    return [
        RoomOut(
            id=room.id,
            name=room.name,
            price_per_night=float(room.price_per_night),
            reservation_ranges=[
                ReservationRangeOut(start_date=br.start_date, end_date=br.end_date)
                for br in room.reservation_ranges
            ],
        )
        for room in rooms
    ]

@router.get("/rooms/{room_id}", response_model=RoomOut)
def get_room(room_id: str, session: Session = Depends(get_session)):
    repo = RoomRepositoryPsql(session)
    room = repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomOut(
        id=room.id,
        name=room.name,
        price_per_night=float(room.price_per_night),
        reservation_ranges=[
            ReservationRangeOut(start_date=br.start_date, end_date=br.end_date)
            for br in room.reservation_ranges
        ],
    )
