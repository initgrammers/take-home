from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from src.shared.infra.db import Base

class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    reservation_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)