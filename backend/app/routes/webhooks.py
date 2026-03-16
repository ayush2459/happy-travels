import hmac, hashlib, json
from fastapi import APIRouter, Request, Header, HTTPException
from app.core.config import settings

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None)
):
    body = await request.body()

    expected_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if expected_signature != x_razorpay_signature:
        raise HTTPException(400, "Invalid webhook signature")

    payload = json.loads(body)

    event = payload.get("event")

    if event == "payment.captured":
        # update booking here
        pass

    return {"status": "ok"}