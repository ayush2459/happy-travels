from fastapi import APIRouter
from pydantic import BaseModel

from app.services.pricing import calculate_price, generate_flights
from app.data.cities import CITY_DATA

router = APIRouter(prefix="/pricing", tags=["Pricing"])


# =========================
# REQUEST MODELS
# =========================

class PriceRequest(BaseModel):
    start: str
    destination: str
    trip_type: str
    flight_class: str
    adults: int = 1
    children: int = 0
    airline_code: str


class FlightSearchRequest(BaseModel):
    start: str
    destination: str
    option: str
    adults: int = 1
    children: int = 0


# =========================
# 💰 PRICE CALCULATOR
# =========================

@router.post("/")
def get_price(req: PriceRequest):

    amount = calculate_price(
        start=req.start,
        destination=req.destination,
        trip_type=req.trip_type,
        flight_class=req.flight_class,
        adults=req.adults,
        children=req.children,
        airline_code=req.airline_code
    )

    return {"amount": amount}


# =========================
# 🌍 CITIES
# =========================

@router.get("/cities")
def get_cities():
    return [
        {
            "key": city.lower(),
            "name": city,
            "country": data["country"],
        }
        for city, data in CITY_DATA.items()
    ]


# =========================
# ✈️ FLIGHTS SEARCH
# =========================

@router.post("/flights")
def flights(req: FlightSearchRequest):

    flights = generate_flights(
        req.start.lower(),
        req.destination.lower(),
        req.option,  # ✅ CORRECT
    )

    passengers = req.adults + (req.children * 0.75)

    for f in flights:
        f["price"] = int(f["price"] * passengers)

    return flights