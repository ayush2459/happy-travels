from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.booking import Booking

def expire_pending_refunds():
    db: Session = SessionLocal()

    expiry_time = datetime.utcnow() - timedelta(days=7)

    refunds = db.query(Booking).filter(
        Booking.refund_status == "PROCESSING",
        Booking.cancelled_at < expiry_time
    ).all()

    for b in refunds:
        b.refund_status = "FAILED"

    db.commit()
    db.close()