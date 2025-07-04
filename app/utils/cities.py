# app/utils/cities.py

cities = {
    "ACE": "Lanzarote",
    "AHO": "Alghero",
    "BOJ": "Burgas",
    "BRI": "Bari",
    "CFU": "Corfu",
    "CIA": "Rome",
    "CRL": "Brussels-Charleroi",
    "DLM": "Dalaman",
    "DUB": "Dublin",
    "EDI": "Edinburgh",
    "EIN": "Eindhoven",
    "GDN": "Gdansk",
    "JSI": "Skiathos",
    "LBA": "Leeds",
    "MAN": "Manchester",
    "MLA": "Malta",
    "MXP": "Milan",
    "PFO": "Paphos",
    "PMI": "Palma de Mallorca",
    "SKG": "Thessaloniki",
    "SOF": "Sofia",
    "STN": "London-Stansted",
    "TPS": "Trapani",
    "ZAD": "Zadar",
    "BTS": "Bratislava",
    "BGY": "Bergamo",
    "VCE": "Venice",
    "BLQ": "Bologna",
    "KRK": "Krakow",
    "BCN": "Barcelona",
    "PUY": "Pula",
    "MRS": "Marseille",
    "VIE": "Vienna",
    "BRU": "Brussels",
    "FCO": "Rome",
    "ATH": "Athens",
    "CPH": "Copenhagen",
    "OTP": "Bucharest",
    "WAW": "Warsaw",
    "PRG": "Prague",
    "LIS": "Lisbon",
    "MAD": "Madrid",
    "CDG": "Paris-CDG",
    "ORY": "Paris-Orly",
    "BVA": "Paris-Beauvais",
    "AMS": "Amsterdam",
    "DUS": "Düsseldorf",
    "HAM": "Hamburg",
    "CGN": "Cologne",
    "LTN": "London-Luton",
    "LGW": "London-Gatwick",
    "LHR": "London-Heathrow",
    "NYO": "Stockholm-Skavsta",
    "OSL": "Oslo",
    "HEL": "Helsinki",
    "TGD": "Podgorica",
    "RJK": "Rijeka",
    "RMI": "Rimini",
    "BNX": "Banja Luka",
    "IBZ": "Ibiza",
}

def get_city_name(code: str) -> str:
    return cities.get(code.upper(), code)
