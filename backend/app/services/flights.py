import random
import math

from app.data.cities import CITY_COORDS
from app.data.airlines import AIRLINES


# =====================================================
# CONSTANTS
# =====================================================

BASE_PRICE_PER_KM = 12
GST_RATE = 0.18
SECURITY_FEE = 250

CLASS_MULTIPLIER = {
    "ECONOMY": 1.0,
    "BUSINESS": 1.8,
    "FIRST": 2.5
}


# =====================================================
# DISTANCE CALCULATOR
# =====================================================

def calculate_distance(start, destination):

    lat1, lon1, _ = CITY_COORDS[start]
    lat2, lon2, _ = CITY_COORDS[destination]

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2)**2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon/2)**2
    )

    return int(2 * R * math.asin(math.sqrt(a)))


# =====================================================
# PRICE CALCULATOR
# ADD YOUR FUNCTION HERE ✅
# =====================================================

def calculate_price(distance, airline, flight_class):

    base = distance * BASE_PRICE_PER_KM

    class_price = base * CLASS_MULTIPLIER[flight_class]

    airline_price = class_price * airline["base_price_multiplier"]

    subtotal = airline_price + airline["surcharge"] + SECURITY_FEE

    gst = subtotal * GST_RATE

    return int(subtotal + gst)


# =====================================================
# FLIGHT GENERATOR
# ADD flights.append HERE ✅
# =====================================================

def generate_flights(start, destination, flight_class):

    start = start.lower()
    destination = destination.lower()

    distance = calculate_distance(start, destination)

    flights = []

    for airline in AIRLINES:

        price = calculate_price(
            distance,
            airline,
            flight_class
        )

        depart_hour = random.randint(0, 23)
        depart_min = random.choice([0, 15, 30, 45])

        duration_hours = int(distance / 800) + 1

        flights.append({

            "type": "DIRECT",

            "airline": airline["name"],

            "airline_code": airline["code"],

            "airline_type": airline["type"],

            "logo": airline["logo"],

            "price": price,

            "currency": "INR",

            "departure": f"{depart_hour:02}:{depart_min:02}",

            "duration": f"{duration_hours}h",

            "arrival": f"{(depart_hour+duration_hours)%24:02}:{depart_min:02}"

        })

    return flights