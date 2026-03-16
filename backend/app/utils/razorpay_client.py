import razorpay

from app.core.config import settings


# =====================================================
# CREATE RAZORPAY CLIENT
# =====================================================

client = None

if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_SECRET:

    client = razorpay.Client(

        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET)

    )