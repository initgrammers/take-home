from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.shared.infra.db import get_session
from api.schemas import ReservationIn, ReservationOut
from src.reservations.application.create_reservation import CreateReservationUseCase
from src.reservations.infra.reservation_repository_psql import ReservationRepositoryPsql
from src.reservations.domain.reservation import Reservation

router = APIRouter()

@router.post("/reservations", response_model=ReservationOut)
def create_reservation(payload: ReservationIn, session: Session = Depends(get_session)):
    reservation_repo = ReservationRepositoryPsql(session)
    use_case = CreateReservationUseCase(reservation_repo)

    reservation = Reservation(
        id=payload.id,
        room_id=payload.room_id,
        guest_email=payload.guest_email,
        start_date=payload.start_date,
        end_date=payload.end_date,
        status="active",
    )
    created = use_case.execute(reservation)
    return ReservationOut(
        id=created.id,
        room_id=created.room_id,
        guest_email=created.guest_email,
        start_date=created.start_date,
        end_date=created.end_date,
        status=created.status,
    )