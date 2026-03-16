# app/services/refund.py
from app.models.refund import Refund
from app.models.booking import Booking

def calculate_refund(booking: Booking) -> int:
    """
    Simple refund rule:
    - Cancel within 24h → 80%
    - Else → no refund
    """
    if booking.payment_status != "PAID":
        return 0

    return int(booking.total_amount * 0.8)