import math
import random
import uuid
import hashlib

from app.data.cities import CITY_DATA

# =====================================================
# BUILD CITY_COORDS FROM CITY_DATA
# =====================================================

CITY_COORDS = {
    city.lower(): (
        data["lat"],
        data["lon"],
        data["airport"]
    )
    for city, data in CITY_DATA.items()
}

# =====================================================
# REALISTIC PRICING CONSTANTS
# =====================================================

# India domestic: avg ₹5.5/km base (DGCA data, ex-tax)
# International: avg ₹6.5/km base (higher ops cost)
DOMESTIC_BASE_PER_KM   = 5.5
INTERNATIONAL_BASE_PER_KM = 6.5

# Minimum fares (floor price regardless of distance)
DOMESTIC_MIN_FARE      = 1800   # e.g. Delhi–Chandigarh
INTERNATIONAL_MIN_FARE = 8000   # e.g. Delhi–Colombo

# Fuel surcharge (YQ) — flat per sector, realistic Indian aviation
DOMESTIC_FUEL_SURCHARGE      = 850
INTERNATIONAL_FUEL_SURCHARGE = 3500

# Airport / carrier charges per sector
DOMESTIC_CARRIER_CHARGES      = 450
INTERNATIONAL_CARRIER_CHARGES = 1800

# GST — Indian aviation rules
# Economy domestic: 5%, Business/First domestic: 12%
# International: exempt (0%) per IGST rules
GST_ECONOMY_DOMESTIC   = 0.05
GST_PREMIUM_DOMESTIC   = 0.12
GST_INTERNATIONAL      = 0.00

# =====================================================
# CABIN MULTIPLIERS (realistic vs economy base)
# Economy = 1x, Premium Economy = 1.6x,
# Business = 3.2x, First = 5.5x
# =====================================================

FLIGHT_CLASS_MULTIPLIER = {
    "ECONOMY":         1.0,
    "PREMIUM_ECONOMY": 1.6,
    "BUSINESS":        3.2,
    "FIRST":           5.5,
}

PREMIUM_CLASSES = {"BUSINESS", "FIRST", "PREMIUM_ECONOMY"}

# =====================================================
# AIRLINE MULTIPLIERS
# Reflects real positioning: budget vs full-service vs premium
# =====================================================

AIRLINES = [
    {
        "name": "IndiGo",
        "code": "6E",
        "logo": "/logos/indigo.png",
        "multiplier": 0.88,     # budget LCC — cheapest
        "surcharge": 0,
    },
    {
        "name": "SpiceJet",
        "code": "SG",
        "logo": "/logos/spicejet.png",
        "multiplier": 0.90,
        "surcharge": 0,
    },
    {
        "name": "Air India",
        "code": "AI",
        "logo": "/logos/airindia.png",
        "multiplier": 1.05,     # full-service, slightly above base
        "surcharge": 300,
    },
    {
        "name": "Vistara",
        "code": "UK",
        "logo": "/logos/vistara.png",
        "multiplier": 1.15,     # premium domestic
        "surcharge": 500,
    },
    {
        "name": "Emirates",
        "code": "EK",
        "logo": "/logos/emirates.png",
        "multiplier": 1.45,     # premium intl
        "surcharge": 2000,
    },
    {
        "name": "Qatar Airways",
        "code": "QR",
        "logo": "/logos/qatar.png",
        "multiplier": 1.40,
        "surcharge": 1800,
    },
    {
        "name": "Singapore Airlines",
        "code": "SQ",
        "logo": "/logos/singapore.png",
        "multiplier": 1.50,
        "surcharge": 2200,
    },
    {
        "name": "Lufthansa",
        "code": "LH",
        "logo": "/logos/lufthansa.png",
        "multiplier": 1.55,
        "surcharge": 2500,
    },
    {
        "name": "British Airways",
        "code": "BA",
        "logo": "/logos/british_airways.png",
        "multiplier": 1.50,
        "surcharge": 2400,
    },
]

# =====================================================
# INDIAN CITIES — for domestic detection
# =====================================================

INDIAN_CITIES = {
    "delhi", "mumbai", "bangalore", "chennai", "kolkata",
    "hyderabad", "pune", "goa", "jaipur", "ahmedabad",
    "lucknow", "kochi", "chandigarh", "indore", "nagpur",
    "varanasi", "amritsar", "bhopal", "patna", "surat",
    "visakhapatnam", "coimbatore", "trivandrum", "guwahati",
    "srinagar", "udaipur", "dehradun", "rajkot", "jodhpur",
    "mysore", "tirupati", "raipur", "ranchi", "agra",
    "bhubaneswar", "mangalore", "jammu", "leh", "port blair", "imphal",
}

def is_domestic(start: str, destination: str) -> bool:
    return start.lower() in INDIAN_CITIES and destination.lower() in INDIAN_CITIES


# =====================================================
# VALIDATION
# =====================================================

def validate_city(city: str):
    if not city:
        raise ValueError("City cannot be empty")
    city = city.lower()
    if city not in CITY_COORDS:
        raise ValueError(f"City not supported: {city}")
    return city


def get_airline(code: str):
    airline = next((a for a in AIRLINES if a["code"] == code), None)
    if not airline:
        raise ValueError(f"Invalid airline code: {code}")
    return airline


# =====================================================
# DISTANCE CALCULATOR (HAVERSINE)
# =====================================================

def distance_km(start: str, destination: str) -> int:
    start = validate_city(start)
    destination = validate_city(destination)

    lat1, lon1, _ = CITY_COORDS[start]
    lat2, lon2, _ = CITY_COORDS[destination]

    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return int(2 * R * math.asin(math.sqrt(a)))


# =====================================================
# STABLE DEMAND FACTOR
# Returns a consistent multiplier for the same route+date
# so the price doesn't change on every page refresh.
# Range: 0.92 – 1.22 (realistic seat availability pressure)
# =====================================================

def stable_demand_factor(start: str, destination: str, date: str = "") -> float:
    key = f"{start.lower()}:{destination.lower()}:{date}"
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    # Map hash to [0.92, 1.22]
    return 0.92 + (h % 1000) / 1000 * 0.30


# =====================================================
# CORE PRICE ENGINE
# =====================================================

def calculate_price(
    start: str,
    destination: str,
    trip_type: str,
    flight_class: str,
    adults: int,
    children: int,
    airline_code: str,
    date: str = "",
) -> int:

    airline   = get_airline(airline_code)
    distance  = distance_km(start, destination)
    domestic  = is_domestic(start, destination)
    fc        = flight_class.upper()

    # ── Base fare per person ──────────────────────────
    rate      = DOMESTIC_BASE_PER_KM if domestic else INTERNATIONAL_BASE_PER_KM
    base_fare = distance * rate

    # Minimum fare floor
    min_fare  = DOMESTIC_MIN_FARE if domestic else INTERNATIONAL_MIN_FARE
    base_fare = max(base_fare, min_fare)

    # Airline positioning multiplier
    base_fare *= airline["multiplier"]
    base_fare += airline["surcharge"]

    # Cabin multiplier
    base_fare *= FLIGHT_CLASS_MULTIPLIER.get(fc, 1.0)

    # Stable demand pricing (route + date locked)
    base_fare *= stable_demand_factor(start, destination, date)

    # ── Surcharges (per person, per sector) ───────────
    fuel    = DOMESTIC_FUEL_SURCHARGE      if domestic else INTERNATIONAL_FUEL_SURCHARGE
    carrier = DOMESTIC_CARRIER_CHARGES     if domestic else INTERNATIONAL_CARRIER_CHARGES
    base_fare += fuel + carrier

    # ── Passenger count ───────────────────────────────
    # Children (2–11): 90% of adult fare (realistic)
    # Infants (<2): typically 10% but not modelled here
    total = (adults * base_fare) + (children * base_fare * 0.90)

    # ── Round trip: return sector at 95% (slight discount) ──
    if trip_type.upper() in ("ROUND_WAY", "ROUND_TRIP"):
        total *= 1.95

    # ── GST ───────────────────────────────────────────
    if domestic:
        gst_rate = GST_PREMIUM_DOMESTIC if fc in PREMIUM_CLASSES else GST_ECONOMY_DOMESTIC
    else:
        gst_rate = GST_INTERNATIONAL

    total += total * gst_rate

    return int(total)


# =====================================================
# DURATION CALCULATOR
# =====================================================

def calculate_duration(distance: int) -> str:
    # Cruise speed ~820 km/h + 30 min taxi/climb for domestic, 45 min intl
    hours = distance / 820 + (0.5 if distance < 2000 else 0.75)
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"


# =====================================================
# FLIGHT SEARCH GENERATOR
# =====================================================

def generate_flights(start, destination, flight_class, date=""):
    start       = validate_city(start)
    destination = validate_city(destination)
    distance    = distance_km(start, destination)

    flights = []

    for airline in AIRLINES:
        price = calculate_price(
            start=start,
            destination=destination,
            trip_type="ONE_WAY",
            flight_class=flight_class,
            adults=1,
            children=0,
            airline_code=airline["code"],
            date=date,
        )

        flights.append({
            "flight_id":    str(uuid.uuid4()),
            "airline":      airline["name"],
            "airline_code": airline["code"],
            "flight_number": f"{airline['code']}{random.randint(100, 999)}",
            "logo":         airline["logo"],
            "duration":     calculate_duration(distance),
            "price":        price,
            "base_price":   price,   # alias for frontend compatibility
            "currency":     "INR",
            "seats_left":   random.randint(5, 60),
        })

    return flights