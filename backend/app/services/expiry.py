from datetime import datetime
from app.db.session import SessionLocal
from app.models.booking import Booking
from app.models.seat_lock import SeatLock


def expire_booking_by_id(booking_id: int):
    db = SessionLocal()
    try:
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.status == "HOLD"
        ).first()

        if not booking:
            return

        lock = db.query(SeatLock).filter(
            SeatLock.booking_id == booking_id
        ).first()

        if lock and lock.expires_at < datetime.utcnow():
            booking.status = "EXPIRED"
            db.delete(lock)
            db.commit()
    finally:
        db.close()

def expire_all_bookings():
    """
    Cron job – expires ALL bookings whose seat locks have expired.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()

        locks = db.query(SeatLock).filter(
            SeatLock.expires_at < now
        ).all()

        for lock in locks:
            booking = db.query(Booking).filter(
                Booking.id == lock.booking_id,
                Booking.status == "HOLD"
            ).first()

            if booking:
                booking.status = "EXPIRED"
                booking.payment_status = "FAILED"

            db.delete(lock)

        db.commit()
    finally:
        db.close()