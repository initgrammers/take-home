from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.shared.infra.db import Base

class RoomModel(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    price_per_night: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    #booking_dates: Mapped[list[str]] = mapped_column(String(50), nullable=False)

    # reservations = relationship("ReservationModel", back_populates="room", cascade="all, delete-orphan")
    