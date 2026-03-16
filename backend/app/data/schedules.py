from app.data.airlines import AIRLINES

SCHEDULES = [

    # =====================================================
    # INDIA → UAE
    # =====================================================

    {
        "flight_number": "6E203",
        "airline": "IndiGo",
        "airline_code": "6E",

        "from": "delhi",
        "to": "dubai",

        "departure": "04:50",
        "arrival": "07:15",

        "aircraft": "Airbus A320",

        "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    },

    {
        "flight_number": "AI915",
        "airline": "Air India",
        "airline_code": "AI",

        "from": "delhi",
        "to": "dubai",

        "departure": "20:15",
        "arrival": "22:45",

        "aircraft": "Boeing 787",

        "days": ["Mon","Wed","Fri","Sun"]
    },


    # =====================================================
    # INDIA → UK
    # =====================================================

    {
        "flight_number": "BA142",
        "airline": "British Airways",
        "airline_code": "BA",

        "from": "delhi",
        "to": "london",

        "departure": "02:10",
        "arrival": "06:30",

        "aircraft": "Boeing 777",

        "days": ["Tue","Thu","Sat"]
    },


    # =====================================================
    # INDIA → SINGAPORE
    # =====================================================

    {
        "flight_number": "SQ403",
        "airline": "Singapore Airlines",
        "airline_code": "SQ",

        "from": "delhi",
        "to": "singapore",

        "departure": "09:20",
        "arrival": "17:45",

        "aircraft": "Airbus A350",

        "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    },


    # =====================================================
    # UAE → INDIA
    # =====================================================

    {
        "flight_number": "EK510",
        "airline": "Emirates",
        "airline_code": "EK",

        "from": "dubai",
        "to": "delhi",

        "departure": "14:10",
        "arrival": "18:55",

        "aircraft": "Boeing 777",

        "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    },


    # =====================================================
    # INDIA → USA
    # =====================================================

    {
        "flight_number": "AI101",
        "airline": "Air India",
        "airline_code": "AI",

        "from": "delhi",
        "to": "new york",

        "departure": "01:45",
        "arrival": "07:30",

        "aircraft": "Boeing 777",

        "days": ["Mon","Wed","Fri"]
    },

]