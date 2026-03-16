import math
from app.data.cities import CITY_DATA

def calculate_distance(city1, city2):

    c1 = CITY_DATA[city1.lower()]
    c2 = CITY_DATA[city2.lower()]

    lat1, lon1 = c1["lat"], c1["lon"]
    lat2, lon2 = c2["lat"], c2["lon"]

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return R * 2 * math.asin(math.sqrt(a))