from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.shared.infra.db import get_session
from api.schemas import RoomOut
from src.rooms.application.list_room import ListRoomsUseCase
from src.rooms.infra.room_repository_psql import RoomRepositoryPsql

router = APIRouter()

@router.get("/rooms", response_model=list[RoomOut])
def list_rooms(session: Session = Depends(get_session)):
    room_repo = RoomRepositoryPsql(session)
    use_case = ListRoomsUseCase(room_repo)
    data = use_case.execute()
    return [RoomOut(id=room.id, name=room.name, price_per_night=float(room.price_per_night)) for room in data]
