from typing import List
from ..domain.payment import Payment
from ..domain.payment_repository import PaymentRepository

class ListPaymentsUseCase:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    def execute(self) -> List[Payment]:
        return list(self.payment_repo.get_all())