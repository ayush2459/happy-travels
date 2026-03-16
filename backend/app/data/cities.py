# app/data/cities.py

CITY_DATA = {

# ================= INDIA (50) =================

"delhi": {"country": "India", "airport": "DEL", "lat": 28.6139, "lon": 77.2090},
"mumbai": {"country": "India", "airport": "BOM", "lat": 19.0760, "lon": 72.8777},
"bangalore": {"country": "India", "airport": "BLR", "lat": 12.9716, "lon": 77.5946},
"chennai": {"country": "India", "airport": "MAA", "lat": 13.0827, "lon": 80.2707},
"kolkata": {"country": "India", "airport": "CCU", "lat": 22.5726, "lon": 88.3639},
"hyderabad": {"country": "India", "airport": "HYD", "lat": 17.3850, "lon": 78.4867},
"pune": {"country": "India", "airport": "PNQ", "lat": 18.5204, "lon": 73.8567},
"goa": {"country": "India", "airport": "GOI", "lat": 15.2993, "lon": 74.1240},
"jaipur": {"country": "India", "airport": "JAI", "lat": 26.9124, "lon": 75.7873},
"ahmedabad": {"country": "India", "airport": "AMD", "lat": 23.0225, "lon": 72.5714},
"lucknow": {"country": "India", "airport": "LKO", "lat": 26.8467, "lon": 80.9462},
"kochi": {"country": "India", "airport": "COK", "lat": 9.9312, "lon": 76.2673},
"chandigarh": {"country": "India", "airport": "IXC", "lat": 30.7333, "lon": 76.7794},
"indore": {"country": "India", "airport": "IDR", "lat": 22.7196, "lon": 75.8577},
"nagpur": {"country": "India", "airport": "NAG", "lat": 21.1458, "lon": 79.0882},
"varanasi": {"country": "India", "airport": "VNS", "lat": 25.3176, "lon": 82.9739},
"amritsar": {"country": "India", "airport": "ATQ", "lat": 31.6340, "lon": 74.8723},
"bhopal": {"country": "India", "airport": "BHO", "lat": 23.2599, "lon": 77.4126},
"patna": {"country": "India", "airport": "PAT", "lat": 25.5941, "lon": 85.1376},
"surat": {"country": "India", "airport": "STV", "lat": 21.1702, "lon": 72.8311},
"visakhapatnam": {"country": "India", "airport": "VTZ", "lat": 17.6868, "lon": 83.2185},
"coimbatore": {"country": "India", "airport": "CJB", "lat": 11.0168, "lon": 76.9558},
"trivandrum": {"country": "India", "airport": "TRV", "lat": 8.5241, "lon": 76.9366},
"guwahati": {"country": "India", "airport": "GAU", "lat": 26.1445, "lon": 91.7362},
"srinagar": {"country": "India", "airport": "SXR", "lat": 34.0837, "lon": 74.7973},
"udaipur": {"country": "India", "airport": "UDR", "lat": 24.5854, "lon": 73.7125},
"dehradun": {"country": "India", "airport": "DED", "lat": 30.3165, "lon": 78.0322},
"rajkot": {"country": "India", "airport": "RAJ", "lat": 22.3039, "lon": 70.8022},
"jodhpur": {"country": "India", "airport": "JDH", "lat": 26.2389, "lon": 73.0243},
"mysore": {"country": "India", "airport": "MYQ", "lat": 12.2958, "lon": 76.6394},
"tirupati": {"country": "India", "airport": "TIR", "lat": 13.6288, "lon": 79.4192},
"raipur": {"country": "India", "airport": "RPR", "lat": 21.2514, "lon": 81.6296},
"ranchi": {"country": "India", "airport": "IXR", "lat": 23.3441, "lon": 85.3096},
"agra": {"country": "India", "airport": "AGR", "lat": 27.1767, "lon": 78.0081},

# ================= UAE =================

"dubai": {"country": "UAE", "airport": "DXB", "lat": 25.2048, "lon": 55.2708},
"abu dhabi": {"country": "UAE", "airport": "AUH", "lat": 24.4539, "lon": 54.3773},
"sharjah": {"country": "UAE", "airport": "SHJ", "lat": 25.3463, "lon": 55.4209},

# ================= USA (40+) =================

"new york": {"country": "USA", "airport": "JFK", "lat": 40.7128, "lon": -74.0060},
"los angeles": {"country": "USA", "airport": "LAX", "lat": 34.0522, "lon": -118.2437},
"chicago": {"country": "USA", "airport": "ORD", "lat": 41.8781, "lon": -87.6298},
"miami": {"country": "USA", "airport": "MIA", "lat": 25.7617, "lon": -80.1918},
"san francisco": {"country": "USA", "airport": "SFO", "lat": 37.7749, "lon": -122.4194},
"seattle": {"country": "USA", "airport": "SEA", "lat": 47.6062, "lon": -122.3321},
"boston": {"country": "USA", "airport": "BOS", "lat": 42.3601, "lon": -71.0589},
"dallas": {"country": "USA", "airport": "DFW", "lat": 32.7767, "lon": -96.7970},
"atlanta": {"country": "USA", "airport": "ATL", "lat": 33.7490, "lon": -84.3880},
"houston": {"country": "USA", "airport": "IAH", "lat": 29.7604, "lon": -95.3698},
"denver": {"country": "USA", "airport": "DEN", "lat": 39.7392, "lon": -104.9903},

# ================= EUROPE =================

"london": {"country": "UK", "airport": "LHR", "lat": 51.5072, "lon": -0.1276},
"paris": {"country": "France", "airport": "CDG", "lat": 48.8566, "lon": 2.3522},
"berlin": {"country": "Germany", "airport": "BER", "lat": 52.5200, "lon": 13.4050},
"rome": {"country": "Italy", "airport": "FCO", "lat": 41.9028, "lon": 12.4964},
"madrid": {"country": "Spain", "airport": "MAD", "lat": 40.4168, "lon": -3.7038},
"amsterdam": {"country": "Netherlands", "airport": "AMS", "lat": 52.3676, "lon": 4.9041},

# ================= ASIA =================

"singapore": {"country": "Singapore", "airport": "SIN", "lat": 1.3521, "lon": 103.8198},
"tokyo": {"country": "Japan", "airport": "HND", "lat": 35.6762, "lon": 139.6503},
"bangkok": {"country": "Thailand", "airport": "BKK", "lat": 13.7563, "lon": 100.5018},
"seoul": {"country": "South Korea", "airport": "ICN", "lat": 37.5665, "lon": 126.9780},

# ================= AUSTRALIA =================

"sydney": {"country": "Australia", "airport": "SYD", "lat": -33.8688, "lon": 151.2093},
"melbourne": {"country": "Australia", "airport": "MEL", "lat": -37.8136, "lon": 144.9631},

# ================= CANADA =================

"toronto": {"country": "Canada", "airport": "YYZ", "lat": 43.6532, "lon": -79.3832},
"vancouver": {"country": "Canada", "airport": "YVR", "lat": 49.2827, "lon": -123.1207},

}
# =====================================================
# AUTO GENERATE CITY_COORDS FOR PRICING SERVICE
# =====================================================

CITY_COORDS = {

    city: (data["lat"], data["lon"])

    for city, data in CITY_DATA.items()

}