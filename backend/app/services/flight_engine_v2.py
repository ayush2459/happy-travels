import random
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.data.cities import CITY_DATA
from app.data.airlines import AIRLINES
from app.services.flight_engine import (
    distance_km,
    calculate_price,
    calculate_duration
)


# ============================================
# AIRLINE HUB NETWORK
# ============================================

AIRLINE_HUBS = {

    "6E": ["delhi", "mumbai", "bangalore"],

    "AI": ["delhi", "mumbai"],

    "EK": ["dubai"],

    "QR": ["doha"],

    "SQ": ["singapore"],

    "LH": ["frankfurt"],

    "BA": ["london"]
}


# ============================================
# TIMEZONE HELPER
# ============================================

def get_timezone(city):

    return ZoneInfo(
        CITY_DATA[city]["timezone"]
    )


# ============================================
# GENERATE FLIGHT NUMBER
# ============================================

def generate_flight_number(code):

    return f"{code}{random.randint(100,9999)}"


# ============================================
# GENERATE REAL DEPARTURE TIME
# ============================================

def generate_departure(city):

    tz = get_timezone(city)

    now = datetime.now(tz)

    departure = now + timedelta(
        hours=random.randint(2, 48)
    )

    return departure


# ============================================
# GENERATE DIRECT FLIGHT
# ============================================

def generate_direct_flight(start, destination, airline, flight_class):

    start = start.lower()
    destination = destination.lower()

    distance = distance_km(start, destination)

    departure = generate_departure(start)

    duration_hours = distance / 800

    arrival = departure + timedelta(
        hours=duration_hours
    )

    price = calculate_price(
        distance,
        airline,
        flight_class
    )

    return {

        "flight_id": str(uuid.uuid4()),

        "type": "DIRECT",

        "airline": airline["name"],

        "airline_code": airline["code"],

        "flight_number":
            generate_flight_number(
                airline["code"]
            ),

        "logo": airline["logo"],

        "start": start.title(),

        "destination":
            destination.title(),

        "departure_time":
            departure.strftime("%Y-%m-%d %H:%M"),

        "arrival_time":
            arrival.strftime("%Y-%m-%d %H:%M"),

        "duration":
            calculate_duration(distance),

        "price": price,

        "currency": "INR",

        "seats_left":
            random.randint(5, 60),

        "aircraft":
            airline.get(
                "aircraft",
                "Boeing 737"
            )
    }


# ============================================
# GENERATE CONNECTING FLIGHT
# ============================================

def generate_connecting_flight(
    start,
    destination,
    airline,
    flight_class
):

    hubs = AIRLINE_HUBS.get(
        airline["code"],
        []
    )

    if not hubs:
        return None

    hub = random.choice(hubs)

    if hub in [start, destination]:
        return None

    d1 = distance_km(start, hub)
    d2 = distance_km(hub, destination)

    total_distance = d1 + d2

    departure = generate_departure(start)

    layover_time = timedelta(
        hours=random.randint(1,4)
    )

    arrival_hub = departure + timedelta(
        hours=d1/800
    )

    departure_hub = arrival_hub + layover_time

    arrival_final = departure_hub + timedelta(
        hours=d2/800
    )

    price = calculate_price(
        total_distance,
        airline,
        flight_class
    )

    price = int(price * random.uniform(1.05,1.25))

    return {

        "flight_id": str(uuid.uuid4()),

        "type": "CONNECTING",

        "airline": airline["name"],

        "airline_code": airline["code"],

        "flight_number":
            generate_flight_number(
                airline["code"]
            ),

        "start": start.title(),

        "destination":
            destination.title(),

        "layover":
            hub.title(),

        "departure_time":
            departure.strftime("%Y-%m-%d %H:%M"),

        "arrival_time":
            arrival_final.strftime("%Y-%m-%d %H:%M"),

        "duration":
            calculate_duration(
                total_distance
            ),

        "price": price,

        "currency": "INR",

        "seats_left":
            random.randint(5,40)
    }


# ============================================
# SEARCH ENGINE v2
# ============================================

def search_flights_v2(
    start,
    destination,
    flight_class="ECONOMY",
    limit=20
):

    start = start.lower()
    destination = destination.lower()

    flights = []

    for airline in AIRLINES:

        # Direct flight
        flights.append(

            generate_direct_flight(
                start,
                destination,
                airline,
                flight_class
            )
        )

        # Connecting flight
        connecting = generate_connecting_flight(
            start,
            destination,
            airline,
            flight_class
        )

        if connecting:
            flights.append(connecting)

    flights.sort(
        key=lambda x: x["price"]
    )

    return {

        "total": len(flights),

        "results":
            flights[:limit]
    }