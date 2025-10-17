from pydantic import BaseModel

class RoomOut(BaseModel):
    id: str
    name: str
    price_per_night: float