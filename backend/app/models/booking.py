from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Booking(Base):

    __tablename__ = "bookings"

    # PRIMARY KEY
    id = Column(Integer, primary_key=True, index=True)

    # IDENTIFIERS
    pnr = Column(String, unique=True, index=True, nullable=False)
    booking_reference = Column(String, unique=True, index=True, nullable=True)

    # USER RELATION
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # ── TRANSPORT MODE ──────────────────────────────────────────────────────
    # "flight" | "train" | "bus" | "car"
    mode = Column(String, nullable=False, default="flight", index=True)

    # ── ROUTE ───────────────────────────────────────────────────────────────
    start       = Column(String, nullable=False, index=True)
    destination = Column(String, nullable=False, index=True)

    # ── TRIP TYPE ───────────────────────────────────────────────────────────
    trip_type   = Column(String, nullable=False, default="ONE_WAY")
    date        = Column(Date, nullable=False, index=True)
    return_date = Column(Date, nullable=True)

    # ── PASSENGERS ──────────────────────────────────────────────────────────
    adults   = Column(Integer, default=1)
    children = Column(Integer, default=0)
    passenger_name = Column(String, nullable=True)

    # ── FLIGHT FIELDS ────────────────────────────────────────────────────────
    airline_code   = Column(String, nullable=True, index=True)
    aircraft_code  = Column(String, nullable=True)
    flight_class   = Column(String, nullable=True)
    seat           = Column(String, nullable=True, index=True)
    seat_status    = Column(String, default="LOCKED")
    gate           = Column(String, nullable=True)

    # Return-flight fields
    ret_flight_number  = Column(String, nullable=True)
    ret_airline_code   = Column(String, nullable=True)
    ret_departure_time = Column(String, nullable=True)
    ret_arrival_time   = Column(String, nullable=True)
    ret_duration       = Column(String, nullable=True)
    ret_gate           = Column(String, nullable=True)
    ret_seat           = Column(String, nullable=True)
    ret_flight_class   = Column(String, nullable=True)

    # ── TRAIN FIELDS ─────────────────────────────────────────────────────────
    train_name   = Column(String, nullable=True)
    train_number = Column(String, nullable=True)
    train_type   = Column(String, nullable=True)
    berth        = Column(String, nullable=True)
    coach        = Column(String, nullable=True)
    berth_type   = Column(String, nullable=True)

    # Return-train fields
    ret_train_name   = Column(String, nullable=True)
    ret_train_number = Column(String, nullable=True)
    ret_train_type   = Column(String, nullable=True)
    ret_berth        = Column(String, nullable=True)
    ret_coach        = Column(String, nullable=True)
    ret_berth_type   = Column(String, nullable=True)

    # ── BUS FIELDS ───────────────────────────────────────────────────────────
    bus_operator  = Column(String, nullable=True)
    bus_type      = Column(String, nullable=True)
    bus_number    = Column(String, nullable=True)
    bus_seat      = Column(String, nullable=True)
    bus_amenities = Column(String, nullable=True)

    # ── CAR FIELDS ───────────────────────────────────────────────────────────
    car_operator  = Column(String, nullable=True)
    car_model     = Column(String, nullable=True)
    car_category  = Column(String, nullable=True)
    car_distance  = Column(String, nullable=True)
    car_eta       = Column(String, nullable=True)
    car_toll      = Column(String, nullable=True)

    # ── PAYMENT ──────────────────────────────────────────────────────────────
    total_amount         = Column(Integer, nullable=False)
    payment_status       = Column(String, default="PENDING")
    razorpay_order_id    = Column(String, nullable=True)
    razorpay_payment_id  = Column(String, nullable=True)

    # ── BOOKING STATUS ───────────────────────────────────────────────────────
    status = Column(String, default="HOLD")

    # ── TIMESTAMPS ───────────────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ── RELATIONSHIPS ────────────────────────────────────────────────────────
    user = relationship("User", back_populates="bookings")
    seat_locks = relationship(
        "SeatLock",
        back_populates="booking",
        cascade="all, delete-orphan"
    )