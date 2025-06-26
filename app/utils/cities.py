# app/utils/cities.py

cities = {
    "ACE": "Lanzarote",
    "AHO": "Alghero",
    "BOJ": "Burgas",
    "BRI": "Bari",
    "CFU": "Korfu",
    "CIA": "Rím",
    "CRL": "Brusel",
    "DLM": "Dalaman",
    "DUB": "Dublin",
    "EDI": "Edinburgh",
    "EIN": "Eindhoven",
    "GDN": "Gdaňsk",
    "JSI": "Skiathos",
    "LBA": "Leeds",
    "MAN": "Manchester",
    "MLA": "Malta",
    "MXP": "Miláno",
    "PFO": "Pafos",
    "PMI": "Palma de Mallorka",
    "SKG": "Solún",
    "SOF": "Sofia",
    "STN": "Londýn",
    "TPS": "Trapani",
    "ZAD": "Zadar",
    "BTS": "Bratislava"
}

def get_city_name(code: str) -> str:
    return cities.get(code.upper(), code)
