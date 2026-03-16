import os, random, string
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.booking import Booking
from app.models.seat_lock import SeatLock
from app.schemas.booking import BookingIn

from app.services.expiry import expire_booking_by_id
from app.services.pricing import calculate_price
from app.services.aircraft_allocator import assign_aircraft
from app.services.seat_map import generate_seat_map, assign_random_seat
from app.services.flight_engine import distance_km
from app.services.pdf_generator import generate_invoice_pdf
from app.services.ticket_generator import generate_boarding_pass
from app.utils.razorpay_client import client

router = APIRouter(prefix="/bookings", tags=["Bookings"])
os.makedirs("tickets", exist_ok=True)

# ─── schemas ──────────────────────────────────────────────────────────────────

class PaymentVerification(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

class SeatLockIn(BaseModel):
    booking_id: int
    seat: str
    date: str

# ─── helpers ──────────────────────────────────────────────────────────────────

def _pnr():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def _ref():
    return "HT" + ''.join(random.choices(string.digits, k=8))

# ─── MODE PRICE ───────────────────────────────────────────────────────────────

_MODE_BASE_PRICE = {
    "train": 800,
    "bus":   400,
    "car":   1200,
    "flight": 4850,
}

def _compute_amount(data: BookingIn) -> int:
    """
    Flights  → use existing calculate_price service.
    Others   → trust frontend total_amount (already includes GST).
    Fallback → simple heuristic if total_amount is 0.
    """
    if data.mode == "flight":
        try:
            return calculate_price(
                start=data.start.lower(),
                destination=data.destination.lower(),
                trip_type=data.trip_type,
                flight_class=data.flight_class or "ECONOMY",
                adults=data.adults,
                children=data.children,
                airline_code=data.airline_code or "6E",
            )
        except Exception as e:
            print(f"[pricing] flight calc failed: {e}")

    if data.total_amount and data.total_amount > 0:
        return data.total_amount

    base = _MODE_BASE_PRICE.get(data.mode, 2000)
    pax  = max(1, data.adults + data.children)
    mult = 2 if data.trip_type == "ROUND_WAY" else 1
    return base * pax * mult


# ─── GET BOOKING ──────────────────────────────────────────────────────────────

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(404, "Booking not found")
    return b


# ─── CREATE BOOKING (all modes) ───────────────────────────────────────────────

@router.post("/")
def create_booking(data: BookingIn, bg: BackgroundTasks, db: Session = Depends(get_db)):

    total_amount = _compute_amount(data)

    aircraft_code = data.aircraft_code or "A320"
    seat = data.seat

    if data.mode == "flight":
        try:
            dist = distance_km(data.start, data.destination)
            aircraft_code = assign_aircraft(dist)
        except Exception:
            pass
        if not seat:
            try:
                seat_map = generate_seat_map(aircraft_code)
                seat = assign_random_seat(seat_map, data.flight_class or "ECONOMY")
            except Exception:
                seat = "Auto"

    # Create Razorpay order for ALL modes
    try:
        rzp_order = client.order.create({
            "amount":          int(total_amount * 100),
            "currency":        "INR",
            "payment_capture": 1,
            "notes": {
                "mode":  data.mode,
                "start": data.start,
                "dest":  data.destination,
            }
        })
        order_id = rzp_order["id"]
    except Exception as e:
        print(f"[razorpay] create order failed: {e}")
        order_id = None   # frontend will fall back to simulation

    b = Booking(
        pnr=_pnr(),
        booking_reference=_ref(),
        mode=data.mode,
        start=data.start,
        destination=data.destination,
        trip_type=data.trip_type,
        date=data.date,
        return_date=data.return_date,
        adults=data.adults,
        children=data.children,
        passenger_name=data.passenger_name,
        total_amount=total_amount,
        payment_status="PENDING",
        status="HOLD",
        razorpay_order_id=order_id,
        # flight
        airline_code=data.airline_code,
        aircraft_code=aircraft_code,
        flight_class=data.flight_class,
        seat=seat,
        seat_status="LOCKED" if data.mode == "flight" else "N/A",
        # return-flight
        ret_flight_number=data.ret_flight_number,
        ret_airline_code=data.ret_airline_code,
        ret_departure_time=data.ret_departure_time,
        ret_arrival_time=data.ret_arrival_time,
        ret_duration=data.ret_duration,
        ret_seat=data.ret_seat,
        ret_flight_class=data.ret_flight_class,
        # train
        train_name=data.train_name,
        train_number=data.train_number,
        train_type=data.train_type,
        berth=data.berth,
        coach=data.coach,
        berth_type=data.berth_type,
        # return-train
        ret_train_name=data.ret_train_name,
        ret_train_number=data.ret_train_number,
        ret_train_type=data.ret_train_type,
        ret_berth=data.ret_berth,
        ret_coach=data.ret_coach,
        ret_berth_type=data.ret_berth_type,
        # bus
        bus_operator=data.bus_operator,
        bus_type=data.bus_type,
        bus_number=data.bus_number,
        bus_seat=data.bus_seat,
        bus_amenities=data.bus_amenities,
        # car
        car_operator=data.car_operator,
        car_model=data.car_model,
        car_category=data.car_category,
        car_distance=data.car_distance,
        car_eta=data.car_eta,
        car_toll=data.car_toll,
    )

    db.add(b)
    db.commit()
    db.refresh(b)

    if data.mode == "flight" and seat and seat != "Auto":
        try:
            lock = SeatLock(
                booking_id=b.id,
                seat=seat,
                date=data.date,
                expires_at=datetime.utcnow() + timedelta(minutes=10),
            )
            db.add(lock)
            db.commit()
            bg.add_task(expire_booking_by_id, b.id)
        except Exception as e:
            print(f"[seat lock] failed: {e}")

    return {
        "success":        True,
        "booking_id":     b.id,
        "pnr":            b.pnr,
        "order_id":       order_id,
        "amount":         b.total_amount,
        "currency":       "INR",
        "status":         b.status,
        "payment_status": b.payment_status,
        "mode":           b.mode,
    }


# ─── VERIFY PAYMENT (all modes) ───────────────────────────────────────────────

@router.post("/{booking_id}/verify-payment")
def verify_payment(
    booking_id: int,
    payload: PaymentVerification,
    db: Session = Depends(get_db),
):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(404, "Booking not found")

    if b.payment_status == "PAID":
        return {"success": True, "message": "Already paid", "pnr": b.pnr}

    if b.razorpay_order_id and b.razorpay_order_id != payload.razorpay_order_id:
        raise HTTPException(400, "Order ID mismatch")

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id":   payload.razorpay_order_id,
            "razorpay_payment_id": payload.razorpay_payment_id,
            "razorpay_signature":  payload.razorpay_signature,
        })
    except Exception:
        raise HTTPException(400, "Payment verification failed")

    b.payment_status      = "PAID"
    b.status              = "CONFIRMED"
    b.seat_status         = "CONFIRMED"
    b.razorpay_payment_id = payload.razorpay_payment_id

    db.query(SeatLock).filter(SeatLock.booking_id == b.id).delete()
    db.commit()

    if b.mode == "flight":
        try:
            generate_boarding_pass(b, f"tickets/boarding_pass_{b.pnr}.pdf")
        except Exception as e:
            print(f"[ticket gen] {e}")

    return {
        "success":    True,
        "message":    "Payment verified",
        "pnr":        b.pnr,
        "booking_id": b.id,
        "mode":       b.mode,
    }


# ─── LOCK SEAT ────────────────────────────────────────────────────────────────

@router.post("/lock-seat")
def lock_seat(payload: SeatLockIn, db: Session = Depends(get_db)):
    try:
        existing = db.query(SeatLock).filter(
            SeatLock.seat == payload.seat,
            SeatLock.date == datetime.strptime(payload.date, "%Y-%m-%d").date(),
        ).first()
        if existing:
            return {"success": False, "message": "Seat already locked"}
        lock = SeatLock(
            booking_id=payload.booking_id,
            seat=payload.seat,
            date=datetime.strptime(payload.date, "%Y-%m-%d").date(),
            expires_at=datetime.utcnow() + timedelta(minutes=10),
        )
        db.add(lock)
        db.commit()
        return {"success": True, "seat": payload.seat}
    except Exception as e:
        print(f"[lock-seat] {e}")
        return {"success": False, "message": str(e)}


# ─── DOWNLOAD TICKET ─────────────────────────────────────────────────────────

@router.get("/{booking_id}/ticket")
def download_ticket(booking_id: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.payment_status == "PAID",
    ).first()
    if not b:
        raise HTTPException(400, "Ticket available only after payment")
    fp = f"tickets/boarding_pass_{b.pnr}.pdf"
    if os.path.exists(fp):
        os.remove(fp)
    generate_boarding_pass(b, fp)
    return FileResponse(fp, media_type="application/pdf",
                        filename=f"ticket_{b.pnr}.pdf")


# ─── DOWNLOAD INVOICE ────────────────────────────────────────────────────────

@router.get("/{booking_id}/invoice")
def download_invoice(booking_id: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(404, "Booking not found")
    if b.payment_status != "PAID":
        raise HTTPException(403, "Invoice available only after payment")
    pdf = generate_invoice_pdf(b)
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=invoice_{b.pnr}.pdf"},
    )


# ─── CANCEL ──────────────────────────────────────────────────────────────────

@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(404, "Booking not found")
    if b.status == "CANCELLED":
        raise HTTPException(400, "Already cancelled")
    b.status         = "CANCELLED"
    b.seat_status    = "RELEASED"
    b.payment_status = "REFUND_PENDING" if b.payment_status == "PAID" else "CANCELLED"
    db.query(SeatLock).filter(SeatLock.booking_id == b.id).delete()
    db.commit()
    return {"success": True, "status": b.status, "payment_status": b.payment_status}


# ─── REFUND ──────────────────────────────────────────────────────────────────

@router.post("/{booking_id}/refund")
def refund_booking(booking_id: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(404, "Booking not found")
    if b.payment_status not in ["PAID", "REFUND_PENDING"]:
        raise HTTPException(400, "Refund not allowed")
    if not b.razorpay_payment_id:
        raise HTTPException(400, "No payment found")
    try:
        refund = client.refund.create({
            "payment_id": b.razorpay_payment_id,
            "amount": b.total_amount * 100,
        })
        b.payment_status = "REFUNDED"
        b.status = "CANCELLED"
        db.commit()
        return {"success": True, "refund_id": refund["id"]}
    except Exception as e:
        raise HTTPException(400, str(e))


# ─── SEAT MAP ────────────────────────────────────────────────────────────────

@router.get("/{booking_id}/seat-map")
def get_seat_map(booking_id: int, db: Session = Depends(get_db)):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(404, "Booking not found")
    seat_map = generate_seat_map(b.aircraft_code or "A320")
    locks = db.query(SeatLock).filter(SeatLock.date == b.date).all()
    locked = {l.seat for l in locks}
    for s in seat_map:
        if s["seat"] in locked:
            s["available"] = False
    return {"aircraft": b.aircraft_code, "total_seats": len(seat_map), "seats": seat_map}