from pydantic import BaseModel


class PaymentVerify(BaseModel):

    booking_id: int

    razorpay_order_id: str

    razorpay_payment_id: str

    razorpay_signature: str