from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Room:
    id: str 
    name: str 
    price_per_night: Decimal
    #booking_dates: list[str]