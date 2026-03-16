import uuid
import random

from app.data.schedules import SCHEDULES
from app.data.airlines import AIRLINES


def get_airline_logo(code):

    airline = next(
        (a for a in AIRLINES if a["code"] == code),
        None
    )

    return airline["logo"] if airline else None


def search_schedules(start, destination):

    start = start.lower()
    destination = destination.lower()

    results = []

    for flight in SCHEDULES:

        if (
            flight["from"] == start
            and
            flight["to"] == destination
        ):

            results.append({

                "id": str(uuid.uuid4()),

                "flight_number":
                    flight["flight_number"],

                "airline":
                    flight["airline"],

                "airline_code":
                    flight["airline_code"],

                "logo":
                    get_airline_logo(
                        flight["airline_code"]
                    ),

                "aircraft":
                    flight["aircraft"],

                "departure":
                    flight["departure"],

                "arrival":
                    flight["arrival"],

                "days":
                    flight["days"],

                "price":
                    random.randint(5000,45000),

                "currency":
                    "INR",

                "seats_available":
                    random.randint(5,40),

                "terminal":
                    f"T{random.randint(1,3)}",

                "gate":
                    f"G{random.randint(1,40)}"

            })

    return results