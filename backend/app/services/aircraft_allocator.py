import random
from app.data.aircraft import AIRCRAFT


def assign_aircraft(distance):

    suitable = []

    for code, aircraft in AIRCRAFT.items():

        if aircraft["range_km"] >= distance:
            suitable.append(code)

    if not suitable:
        return "B777"

    return random.choice(suitable)


def seats_left(aircraft_code):

    capacity = AIRCRAFT[aircraft_code]["seats"]

    return random.randint(10, capacity - 5)


def aircraft_name(code):

    return AIRCRAFT[code]["name"]