import os
import random
from datetime import datetime, timedelta

import qrcode

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.graphics.barcode import code128
from reportlab.lib.utils import ImageReader


# ============================================================
# AIRLINE DATABASE
# ============================================================

AIRLINES = {
    "6E": {
        "name": "IndiGo",
        "color": "#0a3d91",
        "logo": "assets/logos/indigo.png"
    },
    "AI": {
        "name": "Air India",
        "color": "#b91c1c",
        "logo": "assets/logos/airindia.png"
    },
    "UK": {
        "name": "Vistara",
        "color": "#5b2c6f",
        "logo": "assets/logos/vistara.png"
    },
    "EK": {
        "name": "Emirates",
        "color": "#c62828",
        "logo": "assets/logos/emirates.png"
    },
}


# ============================================================
# HELPERS
# ============================================================

def ensure_folder(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def generate_qr(data, path):
    img = qrcode.make(data)
    img.save(path)


def airport_code(city):
    return city[:3].upper()


def random_gate():
    return f"G{random.randint(1, 40)}"


def random_terminal():
    return f"T{random.randint(1, 3)}"


def random_group():
    return random.choice(["A", "B", "C", "D"])


def random_zone():
    return random.choice(["Zone 1", "Zone 2", "Zone 3"])


def random_aircraft():
    return random.choice([
        "Airbus A320",
        "Boeing 737",
        "Boeing 787 Dreamliner",
        "Airbus A321",
        "Boeing 777"
    ])


def boarding_time(date):
    try:
        d = datetime.strptime(str(date), "%Y-%m-%d")
    except:
        d = datetime.now()

    boarding = d - timedelta(minutes=45)

    return boarding.strftime("%H:%M")


def flight_time():
    h = random.randint(0, 23)
    m = random.choice([0, 15, 30, 45])

    return f"{h:02}:{m:02}"


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_ticket_v4(booking, file_path):

    ensure_folder(file_path)

    airline = AIRLINES.get(
        booking.airline_code,
        AIRLINES["6E"]
    )

    airline_color = HexColor(airline["color"])
    airline_name = airline["name"]

    width, height = A4

    c = canvas.Canvas(file_path, pagesize=A4)

    # =====================================================
    # HEADER
    # =====================================================

    c.setFillColor(airline_color)
    c.rect(0, height - 100, width, 100, fill=1)

    c.setFillColor(white)

    c.setFont("Helvetica-Bold", 26)
    c.drawString(40, height - 60, airline_name)

    c.setFont("Helvetica", 14)
    c.drawString(40, height - 85, "BOARDING PASS")

    # Logo
    logo_path = airline["logo"]

    if os.path.exists(logo_path):

        logo = ImageReader(logo_path)

        c.drawImage(
            logo,
            width - 160,
            height - 90,
            width=120,
            height=50,
            mask="auto"
        )

    # =====================================================
    # ROUTE BIG DISPLAY
    # =====================================================

    c.setFillColor(black)

    c.setFont("Helvetica-Bold", 40)

    c.drawString(
        40,
        height - 180,
        airport_code(booking.start)
    )

    c.drawString(
        300,
        height - 180,
        airport_code(booking.destination)
    )

    c.setFont("Helvetica", 16)

    c.drawString(
        40,
        height - 210,
        booking.start.upper()
    )

    c.drawString(
        300,
        height - 210,
        booking.destination.upper()
    )

    # Arrow
    c.line(150, height - 170, 280, height - 170)

    # =====================================================
    # PASSENGER INFO
    # =====================================================

    passenger = getattr(
        booking,
        "passenger_name",
        "PASSENGER"
    )

    gate = random_gate()
    terminal = random_terminal()
    group = random_group()
    zone = random_zone()
    aircraft = random_aircraft()

    board = boarding_time(booking.date)

    flight = f"{booking.airline_code}{random.randint(100,999)}"

    dep_time = flight_time()

    # Labels
    c.setFont("Helvetica", 12)

    labels = [
        ("Passenger", passenger),
        ("Flight", flight),
        ("Date", str(booking.date)),
        ("Seat", booking.seat),
        ("Gate", gate),
        ("Terminal", terminal),
        ("Boarding", board),
        ("Group", group),
        ("Zone", zone),
        ("Aircraft", aircraft),
        ("PNR", booking.pnr),
    ]

    x = 40
    y = height - 270

    for label, value in labels:

        c.drawString(x, y, label)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x, y - 20, str(value))
        c.setFont("Helvetica", 12)

        x += 160

        if x > 450:
            x = 40
            y -= 60

    # =====================================================
    # QR CODE
    # =====================================================

    qr_path = f"tickets/qr_{booking.pnr}.png"

    qr_data = f"""
    PNR:{booking.pnr}
    NAME:{passenger}
    FROM:{booking.start}
    TO:{booking.destination}
    SEAT:{booking.seat}
    """

    generate_qr(qr_data, qr_path)

    qr = ImageReader(qr_path)

    c.drawImage(
        qr,
        width - 180,
        height - 420,
        width=140,
        height=140
    )

    # =====================================================
    # BARCODE
    # =====================================================

    barcode = code128.Code128(
        booking.pnr,
        barHeight=60,
        barWidth=1.5
    )

    barcode.drawOn(c, 40, height - 420)

    # =====================================================
    # TEAR LINE
    # =====================================================

    c.setDash(3, 3)

    c.line(
        0,
        height - 460,
        width,
        height - 460
    )

    c.setDash()

    # =====================================================
    # FOOTER
    # =====================================================

    c.setFont("Helvetica", 10)

    c.drawString(
        40,
        80,
        "Please arrive 2 hours before departure"
    )

    c.drawString(
        40,
        65,
        "Government ID required"
    )

    c.drawString(
        40,
        50,
        "Happy Travels ✈"
    )

    c.save()

    return file_path