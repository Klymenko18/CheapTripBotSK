import requests
from datetime import datetime
from calendar import monthrange


def search_tickets(month: str, max_price: int, min_price: int = 0):
    year = datetime.now().year
    results = []
    offset = 0
    limit = 64

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    _, last_day = monthrange(year, int(month))

    while True:
        url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
        params = {
            "departureAirportIataCode": "BTS",
            "outboundDepartureDateFrom": f"{year}-{month}-01",
            "outboundDepartureDateTo": f"{year}-{month}-{last_day:02d}",
            "market": "sk-sk",
            "language": "sk",
            "limit": limit,
            "offset": offset,
            "priceValueTo": max_price
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            fares = data.get("fares", [])
        except Exception as e:
            results.append(f"⚠️ Chyba počas požiadavky: {str(e)}")
            break

        if not fares:
            break

        for fare in fares:
            outbound = fare.get("outbound", {})
            price_info = outbound.get("price", {})
            price = price_info.get("value", 999)
            currency = price_info.get("currencyCode", "EUR")

            if price < min_price or price > max_price:
                continue

            departure = outbound.get("departureAirport", {}).get("iataCode", "???")
            arrival = outbound.get("arrivalAirport", {}).get("iataCode", "???")
            date = outbound.get("departureDate", "")[:10]

            booking_url = (
                f"https://www.ryanair.com/gb/en/trip/flights/select?"
                f"adults=1&teens=0&children=0&infants=0&isConnectedFlight=false"
                f"&isReturn=false&discount=0"
                f"&originIata={departure}&destinationIata={arrival}&dateOut={date}"
            )

            text = (
                f"<b>✈️ {departure} → {arrival}</b>\n"
                f"<b>📅 Dátum:</b> {date}\n"
                f"<b>💰 Cena:</b> {price} {currency}\n"
                f"<a href='{booking_url}'>🔗 Zobraziť let</a>"
            )
            results.append(text)

        total = data.get("total", 0)
        offset += limit
        if offset >= total:
            break

    if not results:
        results.append("❌ Nenašli sa žiadne lety v tomto mesiaci.")

    return results


def get_cheapest_from_bratislava(month: str):
    year = datetime.now().year
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    _, last_day = monthrange(year, int(month))

    url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": "BTS",
        "outboundDepartureDateFrom": f"{year}-{month}-01",
        "outboundDepartureDateTo": f"{year}-{month}-{last_day:02d}",
        "market": "sk-sk",
        "language": "sk",
        "limit": 64,
        "offset": 0
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
    except Exception:
        return "⚠️ Nepodarilo sa získať odpoveď zo servera."

    fares = data.get("fares", [])
    if not fares:
        return "❌ Nenašli sa žiadne lety v tomto mesiaci."

    cheapest = min(
        fares,
        key=lambda f: f.get("outbound", {}).get("price", {}).get("value", 999)
    )

    outbound = cheapest.get("outbound", {})
    departure = outbound.get("departureAirport", {}).get("iataCode", "???")
    arrival = outbound.get("arrivalAirport", {}).get("iataCode", "???")
    date = outbound.get("departureDate", "")[:10]
    price = outbound.get("price", {}).get("value", 999)
    currency = outbound.get("price", {}).get("currencyCode", "EUR")

    booking_url = (
        f"https://www.ryanair.com/gb/en/trip/flights/select?"
        f"adults=1&teens=0&children=0&infants=0&isConnectedFlight=false"
        f"&isReturn=false&discount=0"
        f"&originIata={departure}&destinationIata={arrival}&dateOut={date}"
    )

    return (
        f"<b>🟢 Najlacnejší let z Bratislavy ({month}):</b>\n"
        f"<b>✈️ {departure} → {arrival}</b>\n"
        f"<b>📅 Dátum:</b> {date}\n"
        f"<b>💰 Cena:</b> {price} {currency}\n"
        f"<a href='{booking_url}'>🔗 Zobraziť let</a>"
    )
