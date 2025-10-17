from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Payment:
    id: str
    reservation_id: str
    amount: Decimal