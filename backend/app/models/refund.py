# app/models/refund.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String, default="PROCESSING")  # PROCESSING / REFUNDED
    created_at = Column(DateTime, server_default=func.now())