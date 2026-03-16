from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db

from app.models.admin import Admin
from app.models.booking import Booking

from app.auth.dependencies import get_current_user
from app.schemas.admin import AdminRegister, AdminLogin
from app.auth.utils import get_password_hash, verify_password, create_access_token

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ==================================================
# ADMIN GUARD
# ==================================================

def admin_guard(user):

    if not user:
        raise HTTPException(401, "Not authenticated")

    if not hasattr(user, "role"):
        raise HTTPException(403, "Role missing")

    if user.role != "admin":
        raise HTTPException(403, "Admin access required")

# =====================================================
# REGISTER ADMIN
# =====================================================

@router.post("/register")
def register_admin(
    data: AdminRegister,
    db: Session = Depends(get_db)
):

    existing = db.query(Admin).filter(
        Admin.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    admin = Admin(

        name=data.name,

        email=data.email,

        password=get_password_hash(data.password)

    )

    db.add(admin)

    db.commit()

    db.refresh(admin)

    return {

        "success": True,

        "message": "Admin registered successfully",

        "admin_id": admin.id

    }
# ==================================================
# ADMIN LOGIN
# ==================================================

@router.post("/login")
def admin_login(
    data: AdminLogin,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.email == data.email
    ).first()

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(data.password, admin.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({

        "admin_id": admin.id,
        "role": "admin"

    })

    return {

        "success": True,
        "access_token": token,
        "token_type": "bearer"
    }


# ==================================================
# MASTER DASHBOARD
# ==================================================

@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    admin_guard(user)

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


    refunded = db.query(
        func.count(Booking.id)
    ).filter(
        Booking.payment_status == "REFUNDED"
    ).scalar()


    # DAILY REVENUE
    daily_rows = db.query(

        func.date(Booking.created_at),
        func.sum(Booking.total_amount)

    ).filter(
        Booking.payment_status == "PAID"

    ).group_by(
        func.date(Booking.created_at)

    ).all()


    daily_revenue = [

        {
            "date": str(r[0]),
            "amount": r[1]
        }

        for r in daily_rows

    ]


    # MONTHLY REVENUE
    monthly_rows = db.query(

        func.strftime("%Y-%m", Booking.created_at),
        func.sum(Booking.total_amount)

    ).filter(
        Booking.payment_status == "PAID"

    ).group_by(
        func.strftime("%Y-%m", Booking.created_at)

    ).all()


    monthly_revenue = [

        {
            "month": r[0],
            "amount": r[1]
        }

        for r in monthly_rows

    ]


    # BOOKING STATUS
    status_rows = db.query(

        Booking.status,
        func.count(Booking.id)

    ).group_by(
        Booking.status
    ).all()


    status_stats = {

        status: count

        for status, count in status_rows

    }


    return {

        "summary": {

            "total_revenue": total_revenue,
            "total_bookings": total_bookings,
            "confirmed_bookings": confirmed,
            "cancelled_bookings": cancelled,
            "refunded_bookings": refunded

        },

        "daily_revenue": daily_revenue,

        "monthly_revenue": monthly_revenue,

        "booking_status": status_stats

    }


# ==================================================
# REVENUE SUMMARY
# ==================================================

@router.get("/revenue/summary")
def revenue_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    admin_guard(user)

    revenue = db.query(
        func.sum(Booking.total_amount)
    ).filter(
        Booking.payment_status == "PAID"
    ).scalar() or 0


    bookings = db.query(
        func.count(Booking.id)
    ).scalar()


    return {

        "total_revenue": revenue,
        "total_bookings": bookings

    }


# ==================================================
# DAILY REVENUE
# ==================================================

@router.get("/revenue/daily")
def revenue_daily(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    admin_guard(user)

    rows = db.query(

        func.date(Booking.created_at),
        func.sum(Booking.total_amount)

    ).filter(
        Booking.payment_status == "PAID"

    ).group_by(
        func.date(Booking.created_at)

    ).all()


    return [

        {
            "date": str(r[0]),
            "amount": r[1]
        }

        for r in rows

    ]


# ==================================================
# MONTHLY REVENUE
# ==================================================

@router.get("/revenue/monthly")
def revenue_monthly(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    admin_guard(user)

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


# ==================================================
# ALL BOOKINGS
# ==================================================

@router.get("/bookings")
def get_all_bookings(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    admin_guard(user)

    return db.query(Booking).order_by(
        Booking.created_at.desc()
    ).all()


# ==================================================
# BOOKING STATS
# ==================================================

@router.get("/bookings/stats")
def booking_stats(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    admin_guard(user)

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

# =====================================================
# REVENUE OVERVIEW
# =====================================================

@router.get("/revenue-overview")
def revenue_overview(
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
# DAILY REVENUE CHART
# =====================================================

@router.get("/revenue-daily-chart")
def revenue_daily_chart(
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

    ).order_by(
        func.date(Booking.created_at)

    ).all()


    return {

        "labels": [str(r.date) for r in rows],

        "data": [r.amount for r in rows]

    }


# =====================================================
# MONTHLY REVENUE CHART
# =====================================================

@router.get("/revenue-monthly-chart")
def revenue_monthly_chart(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    rows = db.query(

        func.strftime("%Y-%m", Booking.created_at).label("month"),
        func.sum(Booking.total_amount).label("amount")

    ).filter(
        Booking.payment_status == "PAID"

    ).group_by(
        func.strftime("%Y-%m", Booking.created_at)

    ).order_by(
        func.strftime("%Y-%m", Booking.created_at)

    ).all()


    return {

        "labels": [r.month for r in rows],

        "data": [r.amount for r in rows]

    }


# =====================================================
# BOOKING STATUS PIE CHART
# =====================================================

@router.get("/booking-status-chart")
def booking_status_chart(
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

        "labels": [r[0] for r in rows],

        "data": [r[1] for r in rows]

    }


# =====================================================
# TOP ROUTES
# =====================================================

@router.get("/top-routes")
def top_routes(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    rows = db.query(

        Booking.start,
        Booking.destination,
        func.count(Booking.id).label("count")

    ).group_by(
        Booking.start,
        Booking.destination

    ).order_by(
        func.count(Booking.id).desc()

    ).limit(10).all()


    return [

        {
            "route": f"{r.start} → {r.destination}",
            "bookings": r.count
        }

        for r in rows

    ]
@router.get("/debug")
def debug(user=Depends(get_current_user)):
    return {
        "role": getattr(user, "role", None),
        "email": getattr(user, "email", None),
        "id": getattr(user, "id", None)
    }