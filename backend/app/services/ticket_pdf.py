from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_ticket_pdf(booking):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "✈ Happy Travels - Flight Ticket")

    c.setFont("Helvetica", 12)
    y = 760
    fields = {
        "PNR": booking.pnr,
        "From": booking.start,
        "To": booking.destination,
        "Date": str(booking.date),
        "Seat": booking.seat,
        "Passengers": f"{booking.adults} Adults, {booking.children} Children",
        "Amount Paid": f"₹{booking.total_amount}"
    }

    for k, v in fields.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 30

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer