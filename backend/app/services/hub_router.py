import random
from app.data.hubs import AIRLINE_HUBS


def get_layover(airline_code, start, destination):

    hubs = AIRLINE_HUBS.get(airline_code, [])

    valid = [
        hub for hub in hubs
        if hub != start and hub != destination
    ]

    if not valid:
        return None

    return random.choice(valid)