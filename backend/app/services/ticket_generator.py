from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.graphics.barcode import code128


def generate_boarding_pass(booking, file_path):
    print("🔥 FINAL CLEAN AIRLINE VERSION 🔥")

    width = 1100
    height = 420

    # ===== SAFE DATA =====
    passenger = (booking.passenger_name or "PASSENGER").upper()
    start = (booking.start or "BOSTON").upper()
    destination = (booking.destination or "NEW YORK").upper()
    seat = booking.seat or "1A"
    gate = "03"
    pnr = booking.pnr or "PH2VD8"
    flight = f"{booking.airline_code or 'AI'}002"
    date = booking.date.strftime("%d %b %Y").upper()

    c = canvas.Canvas(file_path, pagesize=(width, height))

    # ===== COLORS =====
    RED = HexColor("#DA291C")
    GOLD = HexColor("#C9A227")
    DARK = HexColor("#111111")
    GREY = HexColor("#666666")
    LIGHT_GREY = HexColor("#F4F4F4")

    # ===== MAIN BACKGROUND =====
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # ===== TOP RED STRIP =====
    c.setFillColor(RED)
    c.rect(0, height - 15, width, 10, fill=1, stroke=0)

    # ===== LOGO =====
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(GOLD)
    c.drawString(60, height - 70, "AIR INDIA")

    # ===== BOARDING PASS TITLE =====
    c.setFont("Helvetica", 16)
    c.setFillColor(GREY)
    c.drawString(60, height - 100, "BOARDING PASS")

    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(60, height - 108, 720, height - 108)

    # ===== PASSENGER NAME =====
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(DARK)
    c.drawString(60, height - 150, passenger)

    # ===== ROUTE =====
    c.setFont("Helvetica", 12)
    c.setFillColor(GREY)
    c.drawString(60, height - 185, "FROM")
    c.drawString(300, height - 185, "TO")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(DARK)
    c.drawString(60, height - 205, start)
    c.drawString(300, height - 205, destination)

    # ===== INFO GRID =====
    y = height - 250

    labels = ["DATE", "FLIGHT", "SEAT", "GATE"]
    values = [date, flight, seat, gate]
    x_positions = [60, 220, 360, 460]

    c.setFont("Helvetica", 11)
    c.setFillColor(GREY)
    for i, label in enumerate(labels):
        c.drawString(x_positions[i], y, label)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(DARK)
    for i, value in enumerate(values):
        c.drawString(x_positions[i], y - 20, value)

    # ===== BARCODE =====
    barcode = code128.Code128(pnr, barHeight=45, barWidth=1.2)
    barcode.drawOn(c, 60, 80)

    # ===== PERFORATION LINE =====
    c.setStrokeColor(LIGHT_GREY)
    c.setLineWidth(2)
    dot_y = 30
    while dot_y < height - 30:
        c.circle(800, dot_y, 2, fill=1, stroke=0)
        dot_y += 14

    # ===== RIGHT STUB (CLEAN + WIDE) =====
    stub_left = 820

    c.setFillColor(RED)
    c.rect(stub_left, 0, width - stub_left, height, fill=1, stroke=0)

    # ===== STUB CONTENT =====
    c.setFillColor(HexColor("#FFFFFF"))

    c.setFont("Helvetica-Bold", 20)
    c.drawString(stub_left + 40, height - 80, passenger)

    c.setFont("Helvetica", 14)
    c.drawString(stub_left + 40, height - 120, start)
    c.drawString(stub_left + 40, height - 145, "→ " + destination)
    c.drawString(stub_left + 40, height - 180, "SEAT  " + seat)
    c.drawString(stub_left + 40, height - 205, "GATE  " + gate)

    c.save()