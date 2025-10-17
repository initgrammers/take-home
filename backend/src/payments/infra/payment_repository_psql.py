from typing import Sequence, Optional
from decimal import Decimal
from sqlalchemy.orm import Session

from ..domain.payment import Payment
from ..domain.payment_repository import PaymentRepository
from .payment_model_psql import PaymentModel

class PaymentRepositoryPsql(PaymentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[Payment]:
        rows = self.session.query(PaymentModel).all()
        return [
            Payment(
                id=row.id,
                reservation_id=row.reservation_id,
                amount=Decimal(str(row.amount)),
            )
            for row in rows
        ]

    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        row = self.session.get(PaymentModel, payment_id)
        if not row:
            return None
        return Payment(
            id=row.id,
            reservation_id=row.reservation_id,
            amount=Decimal(str(row.amount)),
        )

    def create(self, payment: Payment) -> Payment:
        row = PaymentModel(
            id=payment.id,
            reservation_id=payment.reservation_id,
            amount=payment.amount,
        )
        self.session.add(row)
        self.session.flush()
        return Payment(
            id=row.id,
            reservation_id=row.reservation_id,
            amount=Decimal(str(row.amount)),
        )