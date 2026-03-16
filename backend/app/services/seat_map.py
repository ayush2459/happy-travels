import random
from app.data.aircraft import AIRCRAFT


# =====================================================
# GENERATE FULL SEAT MAP FROM AIRCRAFT LAYOUT
# =====================================================

def generate_seat_map(aircraft_code: str):

    aircraft = AIRCRAFT.get(aircraft_code)

    if not aircraft:
        raise ValueError("Invalid aircraft")

    layout = aircraft["layout"]

    seat_map = []

    for cabin_class, (rows, cols) in layout.items():

        for r in range(1, rows + 1):

            for c in range(cols):

                seat_letter = chr(65 + c)

                seat = f"{r}{seat_letter}"

                seat_map.append({

                    "seat": seat,

                    "class": cabin_class,

                    "available": True

                })

    return seat_map


# =====================================================
# RANDOM ASSIGN SEAT BASED ON CLASS
# =====================================================

def assign_random_seat(seat_map, flight_class):

    seats = [
        s for s in seat_map
        if s["class"] == flight_class and s["available"]
    ]

    if not seats:
        raise Exception("No seats available")

    return random.choice(seats)["seat"]