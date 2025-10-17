from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class ReservationRangeOut(BaseModel):
    start_date: date = Field(..., alias="from")
    end_date: date = Field(..., alias="to")
    model_config = ConfigDict(populate_by_name=True)

class RoomOut(BaseModel):
    id: str
    name: str
    price_per_night: float
    reservation_ranges: list[ReservationRangeOut]

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

class PaymentIn(BaseModel):
    id: str
    reservation_id: str
    amount: float