from pydantic import BaseModel
from datetime import date
from typing import Optional


# =============================================================
# CREATE BOOKING INPUT  — all modes unified
# =============================================================
class BookingIn(BaseModel):
    # ── required ──────────────────────────────────────────────
    mode:        str          # "flight" | "train" | "bus" | "car"
    start:       str
    destination: str
    trip_type:   str          # "ONE_WAY" | "ROUND_WAY"
    date:        date
    return_date: Optional[date] = None
    adults:      int          = 1
    children:    int          = 0
    passenger_name: str       = "Passenger"
    total_amount:   int       = 0   # frontend pre-calculated; backend can override

    # ── flight ────────────────────────────────────────────────
    airline_code:  Optional[str] = None
    flight_class:  Optional[str] = None   # ECONOMY | BUSINESS | FIRST | PREMIUM_ECONOMY
    aircraft_code: Optional[str] = None
    seat:          Optional[str] = None

    # return-flight
    ret_flight_number:  Optional[str] = None
    ret_airline_code:   Optional[str] = None
    ret_departure_time: Optional[str] = None
    ret_arrival_time:   Optional[str] = None
    ret_duration:       Optional[str] = None
    ret_seat:           Optional[str] = None
    ret_flight_class:   Optional[str] = None

    # ── train ─────────────────────────────────────────────────
    train_name:   Optional[str] = None
    train_number: Optional[str] = None
    train_type:   Optional[str] = None
    berth:        Optional[str] = None    # e.g. "S1-4"
    coach:        Optional[str] = None    # e.g. "S1"
    berth_type:   Optional[str] = None    # LB | MB | UB | SL | SU

    # return-train
    ret_train_name:   Optional[str] = None
    ret_train_number: Optional[str] = None
    ret_train_type:   Optional[str] = None
    ret_berth:        Optional[str] = None
    ret_coach:        Optional[str] = None
    ret_berth_type:   Optional[str] = None

    # ── bus ───────────────────────────────────────────────────
    bus_operator:  Optional[str] = None
    bus_type:      Optional[str] = None
    bus_number:    Optional[str] = None
    bus_seat:      Optional[str] = None
    bus_amenities: Optional[str] = None

    # ── car ───────────────────────────────────────────────────
    car_operator: Optional[str] = None
    car_model:    Optional[str] = None
    car_category: Optional[str] = None
    car_distance: Optional[str] = None
    car_eta:      Optional[str] = None
    car_toll:     Optional[str] = None


# =============================================================
# CANCEL INPUT
# =============================================================
class Cancel(BaseModel):
    booking_id: int


# =============================================================
# BOOKING RESPONSE
# =============================================================
class BookingResponse(BaseModel):
    id:             int
    pnr:            str
    mode:           str
    start:          str
    destination:    str
    trip_type:      str
    date:           date
    adults:         int
    children:       int
    total_amount:   int
    status:         str
    payment_status: str
    razorpay_order_id: Optional[str] = None

    class Config:
        from_attributes = True