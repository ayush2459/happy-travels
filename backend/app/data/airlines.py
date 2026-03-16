# =====================================================
# ✈️ PRODUCTION AIRLINES DATABASE
# Includes Domestic + International carriers
# =====================================================

AIRLINES = [

    # =====================================================
    # 🇮🇳 INDIA DOMESTIC AIRLINES
    # =====================================================

    {
        "name": "IndiGo",
        "code": "6E",
        "logo": "/logos/indigo.png",
        "type": "LOW_COST",
        "base_price_multiplier": 1.0,
        "surcharge": 500,
        "aircraft": ["A320", "A321", "ATR 72"]
    },

    {
        "name": "Air India",
        "code": "AI",
        "logo": "/logos/airindia.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 1.25,
        "surcharge": 900,
        "aircraft": ["A320", "A321", "B777", "B787"]
    },

    {
        "name": "Air India Express",
        "code": "IX",
        "logo": "/logos/airindia_express.png",
        "type": "LOW_COST",
        "base_price_multiplier": 1.1,
        "surcharge": 600,
        "aircraft": ["B737"]
    },

    {
        "name": "Akasa Air",
        "code": "QP",
        "logo": "/logos/akasa.png",
        "type": "LOW_COST",
        "base_price_multiplier": 1.05,
        "surcharge": 550,
        "aircraft": ["B737 MAX"]
    },

    {
        "name": "SpiceJet",
        "code": "SG",
        "logo": "/logos/spicejet.png",
        "type": "LOW_COST",
        "base_price_multiplier": 1.0,
        "surcharge": 500,
        "aircraft": ["B737", "Q400"]
    },

    {
        "name": "Alliance Air",
        "code": "9I",
        "logo": "/logos/alliance_air.png",
        "type": "REGIONAL",
        "base_price_multiplier": 0.9,
        "surcharge": 400,
        "aircraft": ["ATR 72"]
    },

    {
        "name": "Star Air",
        "code": "S5",
        "logo": "/logos/star_air.png",
        "type": "REGIONAL",
        "base_price_multiplier": 0.95,
        "surcharge": 450,
        "aircraft": ["Embraer ERJ145"]
    },

    {
        "name": "FlyBig",
        "code": "S9",
        "logo": "/logos/flybig.png",
        "type": "REGIONAL",
        "base_price_multiplier": 0.85,
        "surcharge": 350,
        "aircraft": ["ATR 72"]
    },


    # =====================================================
    # 🌍 MIDDLE EAST
    # =====================================================

    {
        "name": "Emirates",
        "code": "EK",
        "logo": "/logos/emirates.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.2,
        "surcharge": 2500,
        "aircraft": ["A380", "B777"]
    },

    {
        "name": "Qatar Airways",
        "code": "QR",
        "logo": "/logos/qatar.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.3,
        "surcharge": 2600,
        "aircraft": ["A350", "B777", "B787"]
    },

    {
        "name": "Etihad Airways",
        "code": "EY",
        "logo": "/logos/etihad.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.1,
        "surcharge": 2400,
        "aircraft": ["A320", "A350", "B787"]
    },


    # =====================================================
    # 🌏 ASIA
    # =====================================================

    {
        "name": "Singapore Airlines",
        "code": "SQ",
        "logo": "/logos/singapore.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.3,
        "surcharge": 2700,
        "aircraft": ["A350", "A380", "B787"]
    },

    {
        "name": "Thai Airways",
        "code": "TG",
        "logo": "/logos/thai.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.0,
        "surcharge": 2200,
        "aircraft": ["A320", "A350", "B777"]
    },

    {
        "name": "Malaysia Airlines",
        "code": "MH",
        "logo": "/logos/malaysia.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 1.9,
        "surcharge": 2100,
        "aircraft": ["A330", "B737", "A350"]
    },


    # =====================================================
    # 🇪🇺 EUROPE
    # =====================================================

    {
        "name": "Lufthansa",
        "code": "LH",
        "logo": "/logos/lufthansa.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.4,
        "surcharge": 2800,
        "aircraft": ["A320", "A350", "B747"]
    },

    {
        "name": "British Airways",
        "code": "BA",
        "logo": "/logos/british_airways.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.3,
        "surcharge": 2700,
        "aircraft": ["A320", "A380", "B777"]
    },

    {
        "name": "Air France",
        "code": "AF",
        "logo": "/logos/airfrance.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.2,
        "surcharge": 2600,
        "aircraft": ["A320", "A350", "B777"]
    },

    {
        "name": "KLM Royal Dutch",
        "code": "KL",
        "logo": "/logos/klm.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.1,
        "surcharge": 2500,
        "aircraft": ["B737", "B787"]
    },


    # =====================================================
    # 🇺🇸 USA
    # =====================================================

    {
        "name": "United Airlines",
        "code": "UA",
        "logo": "/logos/united.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.5,
        "surcharge": 2900,
        "aircraft": ["B737", "B777", "B787"]
    },

    {
        "name": "Delta Air Lines",
        "code": "DL",
        "logo": "/logos/delta.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.4,
        "surcharge": 2800,
        "aircraft": ["A320", "A350", "B767"]
    },

    {
        "name": "American Airlines",
        "code": "AA",
        "logo": "/logos/american.png",
        "type": "FULL_SERVICE",
        "base_price_multiplier": 2.4,
        "surcharge": 2800,
        "aircraft": ["A320", "B737", "B777"]
    }

]