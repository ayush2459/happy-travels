import math
import random
import uuid
from datetime import datetime, timedelta

from app.data.cities import CITY_DATA
from app.data.airlines import AIRLINES


BASE_PRICE_PER_KM = 12
GST_RATE = 0.18
SECURITY_FEE = 350

CLASS_MULTIPLIER = {
    "ECONOMY": 1.0,
    "BUSINESS": 1.8,
    "FIRST": 2.5
}


AIRCRAFT = [
    "Airbus A320",
    "Airbus A321",
    "Airbus A330",
    "Airbus A350",
    "Boeing 737",
    "Boeing 777",
    "Boeing 787"
]


# =====================================
# DISTANCE CALCULATION
# =====================================

def distance_km(start: str, destination: str):

    start = start.lower().strip()
    destination = destination.lower().strip()

    if start not in CITY_DATA:
        raise ValueError(f"City not found: {start}")

    if destination not in CITY_DATA:
        raise ValueError(f"City not found: {destination}")

    c1 = CITY_DATA[start]
    c2 = CITY_DATA[destination]

    lat1, lon1 = c1["lat"], c1["lon"]
    lat2, lon2 = c2["lat"], c2["lon"]

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    return int(2 * R * math.asin(math.sqrt(a)))


# =====================================
# PRICE ENGINE
# =====================================

def calculate_price(
    start: str,
    destination: str,
    trip_type: str,
    flight_class: str,
    adults: int,
    children: int,
    airline_code: str
):

    airline = next(
        (a for a in AIRLINES if a["code"] == airline_code),
        None
    )

    if not airline:
        raise ValueError("Invalid airline")

    distance = distance_km(start, destination)

    base = distance * BASE_PRICE_PER_KM

    class_price = base * CLASS_MULTIPLIER.get(flight_class, 1)

    airline_price = class_price * airline["base_price_multiplier"]

    subtotal = airline_price + airline["surcharge"] + SECURITY_FEE

    gst = subtotal * GST_RATE

    total = subtotal + gst

    total *= adults + (children * 0.6)

    if trip_type == "ROUND_TRIP":
        total *= 2

    return int(total)


# =====================================
# DURATION CALCULATOR
# =====================================

def calculate_duration(distance):

    minutes = int((distance / 800) * 60)

    hours = minutes // 60
    mins = minutes % 60

    return {
        "duration": f"{hours}h {mins}m",
        "duration_minutes": minutes
    }


# =====================================
# TIME GENERATOR
# =====================================

def generate_time(distance):

    departure = datetime.now() + timedelta(
        hours=random.randint(1, 24)
    )

    duration_hours = distance / 800

    arrival = departure + timedelta(
        hours=duration_hours
    )

    return {

        "departure":
            departure.strftime("%H:%M"),

        "arrival":
            arrival.strftime("%H:%M")
    }


# =====================================
# DIRECT FLIGHTS
# =====================================

def generate_direct(start, destination, flight_class):

    start = start.lower()
    destination = destination.lower()

    distance = distance_km(start, destination)

    flights = []

    for airline in AIRLINES:

        price = calculate_price(
            start,
            destination,
            "ONE_WAY",
            flight_class,
            1,
            0,
            airline["code"]
        )

        duration_data = calculate_duration(distance)

        time = generate_time(distance)

        flights.append({

            "id": str(uuid.uuid4()),

            "flight_id": str(uuid.uuid4()),

            "type": "DIRECT",

            "airline": airline["name"],

            "airline_code": airline["code"],

            "flight_number":
                f"{airline['code']}{random.randint(100,999)}",

            "logo": airline["logo"],

            "aircraft":
                random.choice(AIRCRAFT),

            "duration":
                duration_data["duration"],

            "duration_minutes":
                duration_data["duration_minutes"],

            "distance": distance,

            "price": price,

            "currency": "INR",

            "seats_left":
                random.randint(10,120),

            "departure":
                time["departure"],

            "arrival":
                time["arrival"]
        })

    return flights


# =====================================
# CONNECTING FLIGHTS
# =====================================

def generate_connecting(start, destination, flight_class):

    hubs = ["dubai", "delhi", "london", "singapore"]

    layover = random.choice(hubs)

    if layover == start or layover == destination:
        return []

    d1 = distance_km(start, layover)
    d2 = distance_km(layover, destination)

    total_distance = d1 + d2

    airline = random.choice(AIRLINES)

    price = calculate_price(
        start,
        destination,
        "ONE_WAY",
        flight_class,
        1,
        0,
        airline["code"]
    )

    price = int(price * random.uniform(1.05, 1.25))

    duration_data = calculate_duration(total_distance)

    time = generate_time(total_distance)

    return [{

        "flight_id": str(uuid.uuid4()),

        "type": "CONNECTING",

        "airline": airline["name"],

        "airline_code": airline["code"],

        "flight_number":
            f"{airline['code']}{random.randint(100,999)}",

        "logo": airline["logo"],

        "layover": layover.title(),

        "duration":
            duration_data["duration"],

        "duration_minutes":
            duration_data["duration_minutes"],

        "distance": total_distance,

        "price": price,

        "currency": "INR",

        "seats_left":
            random.randint(5,40),

        "departure":
            time["departure"],

        "arrival":
            time["arrival"]
    }]


# =====================================
# SEARCH ENGINE
# =====================================

def search_flights(start, destination, flight_class="ECONOMY", sort="price", page=1, limit=20):

    flights = []

    flights.extend(generate_direct(start, destination, flight_class))

    flights.extend(generate_connecting(start, destination, flight_class))

    if sort == "price":
        flights.sort(key=lambda x: x["price"])

    start_index = (page - 1) * limit
    end_index = start_index + limit

    return {

        "total": len(flights),

        "page": page,

        "limit": limit,

        "results":
            flights[start_index:end_index]
    }