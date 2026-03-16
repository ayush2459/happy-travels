from fastapi_mail import MessageSchema
from app.core.email import fast_mail


async def send_ticket_email(email, booking, ticket_bytes):

    message = MessageSchema(

        subject="Your Flight Ticket - Happy Travels",

        recipients=[email],

        body=f"""
        Your booking is confirmed.

        PNR: {booking.pnr}
        Route: {booking.start} → {booking.destination}

        Ticket attached.
        """,

        subtype="plain",

        attachments=[
            {
                "file": ticket_bytes,
                "filename": f"ticket_{booking.pnr}.pdf",
                "mime_type": "application/pdf"
            }
        ]
    )

    await fast_mail.send_message(message)