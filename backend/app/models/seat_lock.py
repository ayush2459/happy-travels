from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class SeatLock(Base):

    __tablename__ = "seat_locks"

    id = Column(Integer, primary_key=True)

    booking_id = Column(Integer, ForeignKey("bookings.id"))

    seat = Column(String, nullable=False)

    date = Column(Date, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


    # ✅ THIS FIXES YOUR ERROR
    booking = relationship(
        "Booking",
        back_populates="seat_locks"
    )