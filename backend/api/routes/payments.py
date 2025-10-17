from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.shared.infra.db import get_session
from api.schemas import PaymentOut
from src.payments.application.list_payment import ListPaymentsUseCase
from src.payments.infra.payment_repository_psql import PaymentRepositoryPsql

router = APIRouter()

@router.get("/payments", response_model=list[PaymentOut])
def list_payments(session: Session = Depends(get_session)):
    payment_repo = PaymentRepositoryPsql(session)
    use_case = ListPaymentsUseCase(payment_repo)
    data = use_case.execute()
    return [PaymentOut(id=p.id, reservation_id=p.reservation_id, amount=float(p.amount)) for p in data]