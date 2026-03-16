import uuid
import random

from app.data.airlines import AIRLINES
from app.data.cities import CITY_DATA

from app.services.aircraft_allocator import (
    assign_aircraft,
    seats_left
)

from app.services.airline_scheduler import (
    generate_schedule
)

from app.services.hub_router import (
    get_layover
)

from app.services.pricing import calculate_price


# ===================================
# DISTANCE
# ===================================

def distance_km(start, destination):

    import math

    c1 = CITY_DATA[start]
    c2 = CITY_DATA[destination]

    lat1, lon1 = c1["lat"], c1["lon"]
    lat2, lon2 = c2["lat"], c2["lon"]

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2)**2
    )

    return int(2 * R * math.asin(math.sqrt(a)))


# ===================================
# DIRECT FLIGHTS
# ===================================

def generate_direct(start, destination, flight_class):

    flights = []

    distance = distance_km(start, destination)

    for airline in AIRLINES:

        aircraft = assign_aircraft(distance)

        schedule = generate_schedule(distance)

        price = calculate_price(
            start,
            destination,
            "ONE_WAY",
            flight_class,
            1,
            0,
            airline["code"]
        )

        flights.append({

            "flight_id": str(uuid.uuid4()),

            "flight_number":
                f"{airline['code']}{random.randint(100,999)}",

            "airline": airline["name"],

            "airline_code": airline["code"],

            "aircraft": aircraft,

            "logo": airline["logo"],

            "type": "DIRECT",

            "distance": distance,

            "price": price,

            "currency": "INR",

            "seats_left": seats_left(aircraft),

            **schedule

        })

    return flights


# ===================================
# CONNECTING FLIGHTS
# ===================================

def generate_connecting(start, destination, flight_class):

    flights = []

    airline = random.choice(AIRLINES)

    layover = get_layover(
        airline["code"],
        start,
        destination
    )

    if not layover:
        return []

    d1 = distance_km(start, layover)
    d2 = distance_km(layover, destination)

    total = d1 + d2

    aircraft = assign_aircraft(total)

    schedule = generate_schedule(total)

    price = calculate_price(
        start,
        destination,
        "ONE_WAY",
        flight_class,
        1,
        0,
        airline["code"]
    )

    flights.append({

        "flight_id": str(uuid.uuid4()),

        "flight_number":
            f"{airline['code']}{random.randint(100,999)}",

        "airline": airline["name"],

        "airline_code": airline["code"],

        "aircraft": aircraft,

        "logo": airline["logo"],

        "type": "CONNECTING",

        "layover": layover,

        "distance": total,

        "price": price,

        "currency": "INR",

        "seats_left": seats_left(aircraft),

        **schedule

    })

    return flights


# ===================================
# SEARCH
# ===================================

def search_flights_v3(

    start,
    destination,
    flight_class="ECONOMY",
    page=1,
    limit=20

):

    start = start.lower()
    destination = destination.lower()

    flights = []

    flights.extend(
        generate_direct(start, destination, flight_class)
    )

    flights.extend(
        generate_connecting(start, destination, flight_class)
    )

    flights.sort(key=lambda x: x["price"])

    return {

        "total": len(flights),

        "results":
            flights[(page-1)*limit:page*limit]

    }