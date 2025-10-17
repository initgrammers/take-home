from typing import  Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.shared.infra.db import SessionLocal, engine, Base, is_sqlite
from src.shared.infra.seed import seed_initial_rooms
from api.routes.rooms import router as rooms_router
from api.routes.reservations import router as reservations_router
from api.routes.payments import router as payments_router

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.on_event("startup")
def on_startup():
    # For local dev with SQLite, ensure tables exist
    if is_sqlite:
        Base.metadata.create_all(bind=engine)
    # Seed rooms on first start
    with SessionLocal() as session:
        seed_initial_rooms(session)

app.include_router(rooms_router)
app.include_router(reservations_router)
app.include_router(payments_router)