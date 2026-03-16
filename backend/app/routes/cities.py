from fastapi import APIRouter
from app.data.cities import CITY_DATA

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)


# =====================================================
# GET ALL CITIES
# =====================================================

@router.get("/")
def get_cities():

    cities = []

    for name, data in CITY_DATA.items():

        cities.append({

            "city": name.title(),
            "airport": data["airport"],
            "country": data["country"],
            "lat": data["lat"],
            "lon": data["lon"]

        })

    return {

        "total": len(cities),
        "cities": cities

    }


# =====================================================
# GET SINGLE CITY
# =====================================================

@router.get("/{city}")
def get_city(city: str):

    city = city.lower()

    if city not in CITY_DATA:

        return {"error": "City not found"}

    data = CITY_DATA[city]

    return {

        "city": city.title(),
        "airport": data["airport"],
        "country": data["country"],
        "lat": data["lat"],
        "lon": data["lon"]

    }