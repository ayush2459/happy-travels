# app/routes/seats.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.models.seat_lock import SeatLock
from app.models.booking import Booking

router = APIRouter(prefix="/seats", tags=["Seats"])

LOCK_DURATION_MINUTES = 10


def clear_expired_locks(db: Session):
    db.query(SeatLock).filter(
        SeatLock.expires_at < datetime.utcnow()
    ).delete()
    db.commit()


@router.post("/lock")
def lock_seat(
    booking_id: int,
    flight_id: str,
    seat_no: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    clear_expired_locks(db)

    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id,
        Booking.status == "HOLD",
        Booking.payment_status == "PENDING"
    ).first()

    if not booking:
        raise HTTPException(status_code=400, detail="Booking not payable")

    existing = db.query(SeatLock).filter(
        SeatLock.flight_id == flight_id,
        SeatLock.seat_no == seat_no,
        SeatLock.expires_at > datetime.utcnow()
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Seat already locked")

    lock = SeatLock(
        booking_id=booking_id,
        flight_id=flight_id,
        seat_no=seat_no,
        expires_at=datetime.utcnow() + timedelta(minutes=LOCK_DURATION_MINUTES)
    )

    db.add(lock)
    db.commit()
    db.refresh(lock)

    return {
        "message": "Seat locked",
        "expires_at": lock.expires_at
    }