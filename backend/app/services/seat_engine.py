import random
from app.data.aircraft import AIRCRAFT


def generate_seat_map(aircraft_code):

    aircraft = AIRCRAFT[aircraft_code]

    seat_map = {}

    for seat_class, layout in aircraft["layout"].items():

        rows, cols = layout

        seats = []

        for r in range(1, rows+1):
            for c in "ABCDEF"[:cols]:

                seats.append({

                    "seat": f"{r}{c}",

                    "class": seat_class,

                    "available": random.choice([True, True, True, False])

                })

        seat_map[seat_class] = seats

    return seat_map