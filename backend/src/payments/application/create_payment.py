from decimal import Decimal
from typing import Optional

from ..domain.payment import Payment
from ..domain.payment_repository import PaymentRepository
from src.reservations.domain.reservation_repository import ReservationRepository


class CreatePaymentUseCase:
    def __init__(self, payment_repo: PaymentRepository, reservation_repo: ReservationRepository):
        self.payment_repo = payment_repo
        self.reservation_repo = reservation_repo

    def execute(self, payment: Payment) -> Payment:
        # Validate reservation exists
        reservation = self.reservation_repo.get_by_id(payment.reservation_id)
        if not reservation:
            raise ValueError("Reservation does not exist")
        # Validate reservation is active
        if str(reservation.status).lower() != "active":
            raise ValueError("Reservation is not active")
        # Validate payment not already done for this reservation
        existing: Optional[Payment] = self.payment_repo.get_by_reservation_id(payment.reservation_id)
        if existing:
            raise ValueError("Payment already exists for this reservation")
        # Create payment record
        created = self.payment_repo.create(
            Payment(id=payment.id, reservation_id=payment.reservation_id, amount=Decimal(str(payment.amount)))
        )
        return created