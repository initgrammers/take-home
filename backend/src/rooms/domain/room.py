from dataclasses import dataclass, field
from decimal import Decimal
from datetime import date
from typing import List

@dataclass
class ReservationRange:
    start_date: date
    end_date: date

@dataclass
class Room:
    id: str 
    name: str 
    price_per_night: Decimal
    reservation_ranges: List[ReservationRange] = field(default_factory=list)