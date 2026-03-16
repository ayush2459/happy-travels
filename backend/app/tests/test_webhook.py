import hmac
import hashlib
import json
import requests

# =========================
# CONFIG
# =========================
WEBHOOK_SECRET = "bi3_vGkRytmWTW_"   # same as RAZORPAY_WEBHOOK_SECRET
WEBHOOK_URL = "http://127.0.0.1:8000/payment/webhook"

# =========================
# SAMPLE WEBHOOK PAYLOAD
# =========================
payload = {
    "event": "payment.captured",
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_test_123456",
                "amount": 3582000,
                "currency": "INR",
                "notes": {
                    "receipt": "booking_3"
                }
            }
        }
    }
}

# =========================
# SIGNATURE GENERATION
# =========================
body = json.dumps(payload).encode()

signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Razorpay-Signature": signature
}

# =========================
# SEND REQUEST
# =========================
response = requests.post(
    WEBHOOK_URL,
    data=body,
    headers=headers
)

print("Status Code:", response.status_code)
print("Response:", response.text)