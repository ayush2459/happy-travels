# app/data/aircraft.py

AIRCRAFT = {

    "A320": {
        "name": "Airbus A320",
        "seats": 180,
        "range_km": 6100,
        "speed_kmh": 840,

        "layout": {
            "ECONOMY": (30, 6),
            "BUSINESS": (5, 4)
        }
    },

    "A321": {
        "name": "Airbus A321",
        "seats": 220,
        "range_km": 7400,
        "speed_kmh": 840,

        "layout": {
            "ECONOMY": (35, 6),
            "BUSINESS": (6, 4)
        }
    },

    "B737": {
        "name": "Boeing 737",
        "seats": 189,
        "range_km": 6500,
        "speed_kmh": 830,

        "layout": {
            "ECONOMY": (32, 6),
            "BUSINESS": (4, 4)
        }
    },

    "B777": {
        "name": "Boeing 777",
        "seats": 396,
        "range_km": 15600,
        "speed_kmh": 905,

        "layout": {
            "ECONOMY": (40, 10),
            "BUSINESS": (8, 6),
            "FIRST": (4, 4)
        }
    },

    "B787": {
        "name": "Boeing 787 Dreamliner",
        "seats": 335,
        "range_km": 14100,
        "speed_kmh": 903,

        "layout": {
            "ECONOMY": (35, 9),
            "BUSINESS": (7, 6),
            "FIRST": (4, 4)
        }
    },

    "A350": {
        "name": "Airbus A350",
        "seats": 350,
        "range_km": 16100,
        "speed_kmh": 905,

        "layout": {
            "ECONOMY": (36, 9),
            "BUSINESS": (8, 6),
            "FIRST": (4, 4)
        }
    },

    "A380": {
        "name": "Airbus A380",
        "seats": 615,
        "range_km": 15200,
        "speed_kmh": 900,

        "layout": {
            "ECONOMY": (50, 10),
            "BUSINESS": (10, 6),
            "FIRST": (6, 4)
        }
    }

}