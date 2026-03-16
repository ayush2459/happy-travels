import hmac
import hashlib
import json

from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.booking import Booking
from app.models.seat_lock import SeatLock
from app.schemas.payment import PaymentVerify
from app.utils.razorpay_client import client
from app.core.config import settings


router = APIRouter(prefix="/payment", tags=["Payment"])


# ─── CREATE ORDER ─────────────────────────────────────────────────────────────

@router.post("/create-order")
def create_order(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.status == "HOLD"
    ).first()
    if not booking:
        raise HTTPException(400, "Invalid booking or already processed")
    if booking.payment_status != "PENDING":
        raise HTTPException(400, "Payment already initiated")

    order = client.order.create({
        "amount":   booking.total_amount * 100,
        "currency": "INR",
        "receipt":  f"booking_{booking.id}",
        "notes":    {"booking_id": str(booking.id)}
    })

    booking.razorpay_order_id = order["id"]
    db.commit()

    return {
        "success":  True,
        "order_id": order["id"],
        "amount":   order["amount"],
        "currency": order["currency"]
    }


# ─── VERIFY PAYMENT ───────────────────────────────────────────────────────────

@router.post("/verify")
def verify_payment(data: PaymentVerify, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == data.booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.razorpay_order_id != data.razorpay_order_id:
        raise HTTPException(400, "Order ID mismatch")

    if booking.payment_status == "PAID":
        return {"success": True, "message": "Already verified", "pnr": booking.pnr}

    message = f"{data.razorpay_order_id}|{data.razorpay_payment_id}"
    generated_signature = hmac.new(
        settings.RAZORPAY_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature != data.razorpay_signature:
        raise HTTPException(400, "Invalid payment signature")

    booking.payment_status       = "PAID"
    booking.status               = "CONFIRMED"
    booking.razorpay_payment_id  = data.razorpay_payment_id

    db.query(SeatLock).filter(SeatLock.booking_id == booking.id).delete()
    db.commit()

    return {
        "success":    True,
        "message":    "Payment verified",
        "pnr":        booking.pnr,
        "booking_id": booking.id
    }


# ─── REFUND ───────────────────────────────────────────────────────────────────

@router.post("/refund")
def refund_payment(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.payment_status != "PAID":
        raise HTTPException(400, "Refund not allowed")

    refund = client.payment.refund(booking.razorpay_payment_id)

    booking.payment_status = "REFUNDED"
    booking.status         = "CANCELLED"
    booking.seat_status    = "RELEASED"
    db.commit()

    return {"success": True, "refund_id": refund["id"]}


# ─── WEBHOOK ──────────────────────────────────────────────────────────────────

@router.post("/webhook")
async def webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    try:
        body = await request.body()
        if not body:
            return {"status": "empty"}

        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, x_razorpay_signature):
            return {"status": "invalid signature"}

        payload = json.loads(body)
        event   = payload.get("event")

        if event == "payment.captured":
            payment  = payload["payload"]["payment"]["entity"]
            order_id = payment["order_id"]
            booking  = db.query(Booking).filter(
                Booking.razorpay_order_id == order_id
            ).first()
            if booking:
                booking.payment_status       = "PAID"
                booking.status               = "CONFIRMED"
                booking.razorpay_payment_id  = payment["id"]
                db.query(SeatLock).filter(
                    SeatLock.booking_id == booking.id
                ).delete()
                db.commit()

        return {"status": "ok"}

    except Exception as e:
        print("Webhook error:", str(e))
        return {"status": "error"}


# ─── CONFIG — expose Razorpay key to frontend ─────────────────────────────────

@router.get("/config")
def payment_config():
    return {
        "key": settings.RAZORPAY_KEY_ID,
        "config": {
            "display": {
                "blocks": {
                    "banks": {
                        "name": "Pay via UPI / NetBanking",
                        "instruments": [
                            {"method": "upi"},
                            {"method": "netbanking"}
                        ]
                    },
                    "cards": {
                        "name": "Pay via Card",
                        "instruments": [{"method": "card"}]
                    }
                },
                "sequence": ["block.banks", "block.cards"],
                "preferences": {"show_default_blocks": True}
            }
        }
    }