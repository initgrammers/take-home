from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError  # removed to avoid infra leakage
from src.shared.infra.db import get_session
from api.schemas import ReservationIn, ReservationOut
from src.reservations.application.create_reservation import CreateReservationUseCase
from src.reservations.application.cancel_reservation import CancelReservationUseCase
from src.reservations.infra.reservation_repository_psql import ReservationRepositoryPsql
from src.reservations.domain.reservation import Reservation
from src.rooms.infra.room_repository_psql import RoomRepositoryPsql
from src.rooms.application.room_service import RoomService

router = APIRouter()

@router.post("/reservations", response_model=ReservationOut, status_code=201)
def create_reservation(payload: ReservationIn, session: Session = Depends(get_session)):
    reservation_repo = ReservationRepositoryPsql(session)
    room_repo = RoomRepositoryPsql(session)
    room_service = RoomService(room_repo)
    use_case = CreateReservationUseCase(reservation_repo, room_service)

    reservation = Reservation(
        id=payload.id,
        room_id=payload.room_id,
        guest_email=payload.guest_email,
        start_date=payload.start_date,
        end_date=payload.end_date,
        status="active",
    )
    try:
        created = use_case.execute(reservation)
    except ValueError as e:
        msg = str(e)
        if "room does not exist" in msg:
            raise HTTPException(status_code=404, detail="Room does not exist")
        if "Reservation with this id already exists" in msg:
            raise HTTPException(status_code=409, detail="Reservation with this id already exists")
        raise HTTPException(status_code=422, detail=msg)
    return ReservationOut(
        id=created.id,
        room_id=created.room_id,
        guest_email=created.guest_email,
        start_date=created.start_date,
        end_date=created.end_date,
        status=created.status,
    )

@router.post("/reservations/{reservation_id}/cancel", response_model=ReservationOut)
def cancel_reservation(reservation_id: str, session: Session = Depends(get_session)):
    reservation_repo = ReservationRepositoryPsql(session)
    use_case = CancelReservationUseCase(reservation_repo)
    try:
        updated = use_case.execute(reservation_id)
    except ValueError as e:
        msg = str(e)
        if "reservation not found" in msg:
            raise HTTPException(status_code=404, detail="Reservation not found")
        if "reservation is not active" in msg:
            raise HTTPException(status_code=409, detail="Reservation is not active")
        raise HTTPException(status_code=422, detail=msg)
    return ReservationOut(
        id=updated.id,
        room_id=updated.room_id,
        guest_email=updated.guest_email,
        start_date=updated.start_date,
        end_date=updated.end_date,
        status=updated.status,
    )