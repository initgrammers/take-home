from sqlalchemy.orm import Session
from src.rooms.infra.room_model_psql import RoomModel

SEED_ROOMS = [
    {"id": "7c79f442-fde0-4ef2-9eeb-0dffe92b3a0e", "name":"room1", "price_per_night": 80.0},
    {"id": "df2a67e2-cd30-42de-b3be-ee3d4fc24652", "name":"room2", "price_per_night": 90.0},
    {"id": "e4ec572e-fc15-44a8-bde5-8e692acf9279", "name":"room3", "price_per_night": 100.0},
]

def seed_initial_rooms(session: Session):
    count = session.query(RoomModel).count()
    if count == 0:
        for r in SEED_ROOMS:

            session.add(RoomModel(**r))
        session.commit()