from dataclasses import dataclass
from datetime import date

@dataclass
class Reservation:
    id: str
    room_id: str
    guest_email: str
    start_date: date
    end_date: date
    status: str = "active"