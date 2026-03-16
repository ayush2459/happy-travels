from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.booking import Booking
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/admin/analytics",
    tags=["Admin Analytics"]
)


# =====================================================
# REVENUE OVERVIEW
# =====================================================

@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    total_revenue = db.query(
        func.sum(Booking.total_amount)
    ).filter(
        Booking.payment_status == "PAID"
    ).scalar() or 0


    total_bookings = db.query(
        func.count(Booking.id)
    ).scalar()


    confirmed = db.query(
        func.count(Booking.id)
    ).filter(
        Booking.status == "CONFIRMED"
    ).scalar()


    cancelled = db.query(
        func.count(Booking.id)
    ).filter(
        Booking.status == "CANCELLED"
    ).scalar()


    return {

        "total_revenue": total_revenue,
        "total_bookings": total_bookings,
        "confirmed": confirmed,
        "cancelled": cancelled

    }


# =====================================================
# DAILY REVENUE
# =====================================================

@router.get("/daily-revenue")
def daily_revenue(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    rows = db.query(

        func.date(Booking.created_at).label("date"),
        func.sum(Booking.total_amount).label("amount")

    ).filter(
        Booking.payment_status == "PAID"

    ).group_by(
        func.date(Booking.created_at)

    ).all()


    return [

        {
            "date": str(r.date),
            "amount": r.amount
        }

        for r in rows

    ]


# =====================================================
# MONTHLY REVENUE
# =====================================================

@router.get("/monthly-revenue")
def monthly_revenue(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    rows = db.query(

        func.strftime("%Y-%m", Booking.created_at),
        func.sum(Booking.total_amount)

    ).filter(
        Booking.payment_status == "PAID"

    ).group_by(
        func.strftime("%Y-%m", Booking.created_at)

    ).all()


    return [

        {
            "month": r[0],
            "amount": r[1]
        }

        for r in rows

    ]


# =====================================================
# BOOKING STATUS
# =====================================================

@router.get("/booking-status")
def booking_status(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    rows = db.query(

        Booking.status,
        func.count(Booking.id)

    ).group_by(
        Booking.status
    ).all()


    return {

        status: count

        for status, count in rows

    }