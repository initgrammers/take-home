from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.shared.infra.db import get_session
from api.schemas import PaymentOut, PaymentIn
from src.payments.application.list_payment import ListPaymentsUseCase
from src.payments.application.create_payment import CreatePaymentUseCase
from src.payments.infra.payment_repository_psql import PaymentRepositoryPsql
from src.payments.domain.payment import Payment
from decimal import Decimal
from src.reservations.infra.reservation_repository_psql import ReservationRepositoryPsql

router = APIRouter()

@router.get("/payments", response_model=list[PaymentOut])
def list_payments(session: Session = Depends(get_session)):
    payment_repo = PaymentRepositoryPsql(session)
    use_case = ListPaymentsUseCase(payment_repo)
    data = use_case.execute()
    return [PaymentOut(id=p.id, reservation_id=p.reservation_id, amount=float(p.amount)) for p in data]

@router.post("/payments", response_model=PaymentOut, status_code=201)
def create_payment(payload: PaymentIn, session: Session = Depends(get_session)):
    payment_repo = PaymentRepositoryPsql(session)
    reservation_repo = ReservationRepositoryPsql(session)
    use_case = CreatePaymentUseCase(payment_repo, reservation_repo)
    try:
        created = use_case.execute(
            Payment(id=payload.id, reservation_id=payload.reservation_id, amount=Decimal(str(payload.amount)))
        )
    except ValueError as e:
        msg = str(e)
        if "Reservation does not exist" in msg:
            raise HTTPException(status_code=404, detail="Reservation does not exist")
        if "Reservation is not active" in msg:
            raise HTTPException(status_code=400, detail="Reservation is not active")
        if "Payment already exists" in msg:
            raise HTTPException(status_code=409, detail="Payment already exists for this reservation")
        raise HTTPException(status_code=422, detail=msg)
    return PaymentOut(id=created.id, reservation_id=created.reservation_id, amount=float(created.amount))