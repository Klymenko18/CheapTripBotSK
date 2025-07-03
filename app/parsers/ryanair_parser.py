from datetime import datetime, timedelta
from calendar import monthrange
import requests
from app.utils.cities import get_city_name

def search_tickets(data):
    origin = data.get("origin", "BTS")
    month = data.get("month")
    price_cb = data.get("price")
    return_date = data.get("return_date")
    country = data.get("country")

    year = datetime.now().year

    try:
        month_int = int(month)
        _, last_day = monthrange(year, month_int)
    except (ValueError, TypeError):
        return ["⚠️ Invalid month value. Please start search again."]

    min_price = 0
    max_price = 999
    if price_cb == "30":
        max_price = 30
    elif price_cb == "50":
        min_price = 30
        max_price = 50

    origin_market_map = {
        "BTS": "sk-sk",
        "KSC": "sk-sk",
        "VIE": "at-en",
        "BUD": "hu-hu",
    }
    market = origin_market_map.get(origin, "sk-sk")

    results = []
    offset = 0
    limit = 64

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": origin,
        "outboundDepartureDateFrom": f"{year}-{month}-01",
        "outboundDepartureDateTo": f"{year}-{month}-{last_day:02d}",
        "market": market,
        "language": "sk",
        "limit": limit,
        "offset": offset,
        "priceValueTo": max_price
    }

    while True:
        try:
            response = requests.get(url, params=params, headers=headers)
            data_json = response.json()
            fares = data_json.get("fares", [])
        except Exception as e:
            results.append(f"⚠️ Chyba počas požiadavky: {str(e)}")
            break

        if not fares:
            break

        for fare in fares:
            out = fare.get("outbound", {})
            arrival = out.get("arrivalAirport", {}).get("iataCode", "")
            arrival_country = out.get("arrivalAirport", {}).get("countryCode", "")
            if country and country != "ALL" and arrival_country != country:
                continue

            date = out.get("departureDate", "")[:10]
            price = out.get("price", {}).get("value", 999)
            currency = out.get("price", {}).get("currencyCode", "EUR")

            booking_url = (
                f"https://www.ryanair.com/gb/en/trip/flights/select?"
                f"adults=1&teens=0&children=0&infants=0&isConnectedFlight=false"
                f"&isReturn={bool(return_date)}&discount=0"
                f"&originIata={origin}&destinationIata={arrival}&dateOut={date}"
            )

            if return_date:
                booking_url += f"&dateIn={return_date}"

            text = (
                f"<b>✈️ {get_city_name(origin)} → {get_city_name(arrival)}</b>\n"
                f"<b>📅 Dátum:</b> {date}\n"
                f"<b>💰 Cena:</b> {price} {currency}\n"
                f"<a href='{booking_url}'>🔗 Zobraziť let</a>"
            )
            results.append(text)

        offset += limit
        if offset >= data_json.get("total", 0):
            break

    if not results:
        results.append("❌ Nič sa nenašlo v danom mesiaci.")

    return results


def get_cheapest_from_city(month: str, origin: str):
    year = datetime.now().year
    try:
        month_int = int(month)
        _, last_day = monthrange(year, month_int)
    except (ValueError, TypeError):
        return "⚠️ Invalid month value. Please restart search."

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    origin_market_map = {
        "BTS": "sk-sk",
        "KSC": "sk-sk",
        "VIE": "at-en",
        "BUD": "hu-hu",
    }
    market = origin_market_map.get(origin, "sk-sk")

    url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": origin,
        "outboundDepartureDateFrom": f"{year}-{month}-01",
        "outboundDepartureDateTo": f"{year}-{month}-{last_day:02d}",
        "market": market,
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
        f"adults=1&originIata={departure}&destinationIata={arrival}&dateOut={date}"
    )

    return (
        f"<b>🟢 Najlacnejší let z {get_city_name(origin)}:</b>\n"
        f"<b>✈️ {get_city_name(departure)} → {get_city_name(arrival)}</b>\n"
        f"<b>📅 Dátum:</b> {date}\n"
        f"<b>💰 Cena:</b> {price} {currency}\n"
        f"<a href='{booking_url}'>🔗 Zobraziť let</a>"
    )


def get_cheapest_next_7_days(origin="BTS"):
    today = datetime.now().date()
    results = []

    for i in range(7):
        day = today + timedelta(days=i)
        m = str(day.month).zfill(2)

        daily_results = search_tickets({
            "month": m,
            "origin": origin,
            "price": "all",
            "country": "ALL"
        })

        for r in daily_results:
            if f"{day.year}-{m}-{str(day.day).zfill(2)}" in r:
                results.append((day, r))

    if not results:
        return "❌ Nenašli sa žiadne lety na najbližší týždeň."

    cheapest = min(
        results,
        key=lambda x: float(x[1].split("Cena:</b> ")[1].split(" ")[0].replace(",", "."))
    )

    return f"🟢 Najlacnejší let z najbližších 7 dní:\n{cheapest[1]}"
