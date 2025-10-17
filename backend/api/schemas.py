from pydantic import BaseModel

class RoomOut(BaseModel):
    id: str
    name: str
    price_per_night: float

from datetime import date

class ReservationIn(BaseModel):
    id: str
    room_id: str
    guest_email: str
    start_date: date
    end_date: date

class ReservationOut(BaseModel):
    id: str
    room_id: str
    guest_email: str
    start_date: date
    end_date: date
    status: str

class PaymentOut(BaseModel):
    id: str
    reservation_id: str
    amount: float