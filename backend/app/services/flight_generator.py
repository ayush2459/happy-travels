import random
from app.data.airlines import AIRLINES

def generate_flights(start, destination):

    flights = []

    for airline in AIRLINES:

        flights.append({

            "airline": airline["name"],
            "logo": airline["logo"],
            "flight_number": airline["code"] + str(random.randint(100,999)),
            "departure": "10:30",
            "arrival": "14:30",
            "duration": "4h",
            "seats_available": random.randint(5, 120)

        })

    return flights