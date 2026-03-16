import io
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import colors

from reportlab.graphics.barcode import createBarcodeDrawing

from app.data.airlines import AIRLINES
import qrcode

styles = getSampleStyleSheet()


# =========================================
# HELPERS
# =========================================

def airport_code(city: str) -> str:
    return city[:3].upper()


def get_airline(airline_code: str):
    airline = next(
        (a for a in AIRLINES if a["code"] == airline_code),
        None
    )

    return airline if airline else {
        "name": airline_code,
        "logo": None
    }


# =========================================
# PAGE NUMBER FOOTER
# =========================================

def add_page_number(canvas, doc):
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(580, 15, f"Page {doc.page}")


# =========================================
# MAIN FUNCTION
# =========================================

def generate_invoice_pdf(booking):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    airline = get_airline(booking.airline_code)

    invoice_no = f"HTINV-{datetime.utcnow().strftime('%Y%m%d')}-{booking.id:04}"
    date_str = datetime.utcnow().strftime("%d %b %Y")
    flight_number = f"{booking.airline_code}{booking.id:03}"

    passenger = getattr(booking, "passenger_name", "Passenger")
    razorpay_payment_id = getattr(booking, "razorpay_payment_id", "N/A")
    boarding_group = getattr(booking, "boarding_group", "C")

    # =========================================
    # PREMIUM HEADER BAND
    # =========================================

    brand_color = colors.HexColor("#1f4ea8")

    header_band = Table([[" "]], colWidths=[540], rowHeights=[18])
    header_band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), brand_color)
    ]))

    elements.append(header_band)
    elements.append(Spacer(1, 15))

    # =========================================
    # HEADER SECTION
    # =========================================

    header_table = Table([
        [
            Paragraph(f"<b>{airline['name']}</b>", styles["Heading2"]),
            Paragraph(
                f"""
                <b>TAX INVOICE</b><br/>
                Invoice No: {invoice_no}<br/>
                Date: {date_str}<br/>
                Payment ID: {razorpay_payment_id}
                """,
                ParagraphStyle(
                    name="RightAlign",
                    parent=styles["Normal"],
                    alignment=TA_RIGHT
                )
            )
        ]
    ], colWidths=[270, 270])

    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 25))

    # =========================================
    # QR CODE
    # =========================================

    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(f"{booking.pnr}|{booking.total_amount}|{flight_number}")
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    elements.append(Image(qr_buffer, width=80, height=80))
    elements.append(Spacer(1, 15))

    # =========================================
    # BARCODE (VECTOR SAFE)
    # =========================================

    barcode = createBarcodeDrawing(
        "Code128",
        value=booking.pnr,
        barHeight=30,
        humanReadable=True
    )

    elements.append(barcode)
    elements.append(Spacer(1, 30))

    # =========================================
    # PASSENGER DETAILS
    # =========================================

    elements.append(Paragraph("<b>PASSENGER DETAILS</b>", styles["Heading3"]))
    elements.append(Spacer(1, 10))

    passenger_table = Table([
        ["Passenger", passenger],
        ["PNR", booking.pnr],
        ["Booking Ref", booking.booking_reference],
        ["Boarding Group", boarding_group],
        ["Seat", booking.seat],
        ["Class", booking.flight_class],
    ], colWidths=[150, 350])

    passenger_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.2, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1),
         [colors.white, colors.HexColor("#f7f7f7")]),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))

    elements.append(passenger_table)
    elements.append(Spacer(1, 25))

    # =========================================
    # FLIGHT DETAILS
    # =========================================

    elements.append(Paragraph("<b>FLIGHT DETAILS</b>", styles["Heading3"]))
    elements.append(Spacer(1, 10))

    route = f"{airport_code(booking.start)} → {airport_code(booking.destination)}"

    flight_table = Table([
        ["Airline", airline["name"]],
        ["Flight Number", flight_number],
        ["Route", route],
        ["Departure", booking.start],
        ["Arrival", booking.destination],
        ["Travel Date", str(booking.date)],
    ], colWidths=[150, 350])

    flight_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.2, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1),
         [colors.white, colors.HexColor("#f7f7f7")]),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))

    elements.append(flight_table)
    elements.append(Spacer(1, 25))

    # =========================================
    # PAYMENT BREAKDOWN
    # =========================================

    subtotal = booking.total_amount / 1.18
    gst = booking.total_amount - subtotal

    elements.append(Paragraph("<b>PAYMENT BREAKDOWN</b>", styles["Heading3"]))
    elements.append(Spacer(1, 10))

    payment_table = Table([
        ["Fare Charges", f"₹ {subtotal:.2f}"],
        ["GST (18%)", f"₹ {gst:.2f}"],
        ["Total Paid", f"₹ {booking.total_amount:.2f}"],
    ], colWidths=[350, 150])

    payment_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.2, colors.lightgrey),
        ("BACKGROUND", (0, 2), (-1, 2), colors.whitesmoke),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))

    elements.append(payment_table)
    elements.append(Spacer(1, 40))

    # =========================================
    # FOOTER
    # =========================================

    elements.append(Paragraph(
        "This is a computer generated invoice and does not require signature.",
        styles["Normal"]
    ))

    doc.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)
    return buffer