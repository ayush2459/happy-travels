import uuid
import random
from fastapi import APIRouter, HTTPException, Query

from app.data.cities import CITY_DATA
from app.data.airlines import AIRLINES
from app.services.flight_engine import search_flights as engine_search_flights
from app.services.flight_engine import search_flights as search_schedules
from app.services.flight_engine_v2 import search_flights_v2
from app.services.flight_engine_v3 import search_flights_v3
router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
)

# =========================================================
# AIRCRAFT TYPES
# =========================================================

AIRCRAFT_TYPES = [
    "Airbus A320",
    "Airbus A321",
    "Airbus A330",
    "Airbus A350",
    "Airbus A380",
    "Boeing 737",
    "Boeing 747",
    "Boeing 777",
    "Boeing 787 Dreamliner"
]

# =========================================================
# SEAT MAP GENERATOR (separate endpoint usage)
# =========================================================

def generate_seat_map():

    rows = 30
    cols = ["A", "B", "C", "D", "E", "F"]

    seats = []

    for r in range(1, rows + 1):
        for c in cols:

            seats.append({

                "seat": f"{r}{c}",

                "class": (
                    "FIRST" if r <= 2 else
                    "BUSINESS" if r <= 8 else
                    "ECONOMY"
                ),

                "available": random.choice(
                    [True, True, True, False]
                )
            })

    return seats


# =========================================================
# SEARCH FLIGHTS (MAIN PRODUCTION ENDPOINT)
# =========================================================

@router.get("/search")
def search(

    start: str = Query(...),
    destination: str = Query(...),
    flight_class: str = Query("ECONOMY"),
    sort: str = Query("price"),
    page: int = Query(1),
    limit: int = Query(20)

):

    # normalize inputs
    start = start.lower().strip()
    destination = destination.lower().strip()
    flight_class = flight_class.upper().strip()

    # validation
    if start not in CITY_DATA:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid start city: {start}"
        )

    if destination not in CITY_DATA:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination city: {destination}"
        )

    try:

        result = engine_search_flights(
            start=start,
            destination=destination,
            flight_class=flight_class,
            sort=sort,
            page=page,
            limit=limit
        )

        enriched = []

        for flight in result["results"]:

            enriched.append({

                "id": flight.get("id") or flight.get("flight_id") or str(uuid.uuid4()),

                "flight_number":
                    flight.get("flight_number") or f"{flight['airline_code']}{random.randint(100, 999)}",

                "airline": flight["airline"],

                "airline_code": flight["airline_code"],

                "logo": flight["logo"],

                "aircraft":
                    random.choice(AIRCRAFT_TYPES),

                "type": flight["type"],

                "departure": flight["departure"],

                "arrival": flight["arrival"],

                "duration": flight["duration"],

                "duration_minutes":
                    flight["duration_minutes"],

                "price": flight["price"],

                "currency": flight["currency"],

                "seats_available":
                    random.randint(3, 40),

                "seat_map_available": True
            })

        return {

            "success": True,

            "route":
                f"{start.title()} → {destination.title()}",

            "total": result["total"],

            "page": result["page"],

            "limit": result["limit"],

            "results": enriched
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Flight search failed: {str(e)}"
        )
# =========================================================
# SEAT MAP API
# =========================================================

@router.get("/{flight_id}/seatmap")
def seatmap(flight_id: str):

    return {

        "flight_id": flight_id,

        "aircraft": random.choice(AIRCRAFT_TYPES),

        "total_seats": 180,

        "seat_map": generate_seat_map()
    }
@router.get("/schedule-search")
def schedule_search(
    start: str,
    destination: str
):

    flights = search_schedules(
        start,
        destination
    )

    return {

        "route":
            f"{start} → {destination}",

        "total":
            len(flights),

        "flights":
            flights
    }


# =========================================================
# MULTI CITY SEARCH
# =========================================================

@router.post("/multi-city")
def multi_city(

    cities: list[str],

    flight_class: str = "ECONOMY"

):

    try:

        cities = [c.lower().strip() for c in cities]

        for city in cities:

            if city not in CITY_DATA:
                raise HTTPException(
                    400,
                    f"Invalid city: {city}"
                )

        flights = []

        for i in range(len(cities) - 1):

            segment = engine_search_flights(

                start=cities[i],

                destination=cities[i+1],

                flight_class=flight_class,

                limit=5

            )

            flights.extend(segment["results"])

        return {

            "success": True,

            "route":
                " → ".join(city.title() for city in cities),

            "segments": len(cities) - 1,

            "total_flights": len(flights),

            "flights": flights
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/{flight_id}/seatmap")
def get_seatmap(flight_id: str):

    rows = 30
    cols = ["A","B","C","D","E","F"]

    seats = []

    for r in range(1, rows+1):

        for c in cols:

            seats.append({

                "seat": f"{r}{c}",
                "available": random.choice([True, True, True, False])

            })

    return {
        "flight_id": flight_id,
        "seats": seats

    }
router.get("/search-v2")
def search_v2(
    start: str,
    destination: str,
    flight_class: str = "ECONOMY"
):

    return search_flights_v2(
        start,
        destination,
        flight_class
    )