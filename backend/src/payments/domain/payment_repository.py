from abc import ABC, abstractmethod
from typing import Sequence, Optional
from .payment import Payment

class PaymentRepository(ABC):
    @abstractmethod
    def get_all(self) -> Sequence[Payment]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        raise NotImplementedError

    @abstractmethod
    def create(self, payment: Payment) -> Payment:
        raise NotImplementedError