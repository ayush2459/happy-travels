import random
from datetime import datetime, timedelta


def generate_schedule(distance):

    now = datetime.now()

    departure = now + timedelta(
        hours=random.randint(1, 24)
    )

    speed = 850

    duration_hours = distance / speed

    arrival = departure + timedelta(
        hours=duration_hours
    )

    duration_minutes = int(duration_hours * 60)

    hours = duration_minutes // 60
    mins = duration_minutes % 60

    return {

        "departure": departure.strftime("%H:%M"),

        "arrival": arrival.strftime("%H:%M"),

        "duration": f"{hours}h {mins}m",

        "duration_minutes": duration_minutes

    }