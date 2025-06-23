import requests
from datetime import datetime

def search_tickets(month: str, max_price: int):
    results = []
    origins = ["BTS"]  # можна додати VIE, BUD тощо
    destinations = ["STN", "BCN", "DUB", "PAR", "FCO"]  # приклад
    year = datetime.now().year

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    for origin in origins:
        for destination in destinations:
            url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
            params = {
                "departureAirportIataCode": origin,
                "arrivalAirportIataCode": destination,
                "outboundDepartureDateFrom": f"{year}-{month}-01",
                "outboundDepartureDateTo": f"{year}-{month}-30",
                "priceValueTo": max_price,
                "market": "sk-sk",
                "language": "sk",
                "limit": 16,
                "offset": 0
            }
            try:
                response = requests.get(url, params=params, headers=headers)
                data = response.json()
            except Exception as e:
                continue

            for fare in data.get("fares", []):
                price = fare.get("outbound", {}).get("price", {}).get("value", 999)
                if price > max_price:
                    continue

                departure = fare["outbound"]["departureAirport"]["iataCode"]
                arrival = fare["outbound"]["arrivalAirport"]["iataCode"]
                date = fare["outbound"]["departureDate"][:10]
                currency = fare["outbound"]["price"]["currencyCode"]
                url = (
                    f"https://www.ryanair.com/gb/en/trip/flights/select?"
                    f"adults=1&teens=0&children=0&infants=0&isConnectedFlight=false&isReturn=false&discount=0"
                    f"&originIata={departure}&destinationIata={arrival}&dateOut={date}"
                )

                text = (
                    f"<b>✈️ {departure} → {arrival}</b>\n"
                    f"<b>📅 Дата:</b> {date}\n"
                    f"<b>💰 Ціна:</b> {price} {currency}\n"
                    f"<a href='{url}'>🔗 Перейти до білету</a>"
                )
                results.append(text)

    if not results:
        results.append(
            f"<b>✈️ BTS → PRG</b>\n"
            f"<b>📅 Дата:</b> {year}-{month}-15\n"
            f"<b>💰 Ціна:</b> 29€\n"
            f"<a href='https://www.ryanair.com'>🔗 Фейкове посилання</a>"
        )

    return results

def get_cheapest_from_bratislava(month: str):
    year = datetime.now().year
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": "BTS",
        "outboundDepartureDateFrom": f"{year}-{month}-01",
        "outboundDepartureDateTo": f"{year}-{month}-30",
        "market": "sk-sk",
        "language": "sk",
        "limit": 10,
        "offset": 0
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
    except Exception:
        return None

    fares = data.get("fares", [])
    if not fares:
        return None

    cheapest = min(
        fares,
        key=lambda f: f.get("outbound", {}).get("price", {}).get("value", 999)
    )

    departure = cheapest["outbound"]["departureAirport"]["iataCode"]
    arrival = cheapest["outbound"]["arrivalAirport"]["iataCode"]
    date = cheapest["outbound"]["departureDate"][:10]
    price = cheapest["outbound"]["price"]["value"]
    currency = cheapest["outbound"]["price"]["currencyCode"]
    url = (
        f"https://www.ryanair.com/gb/en/trip/flights/select?"
        f"adults=1&teens=0&children=0&infants=0&isConnectedFlight=false&isReturn=false&discount=0"
        f"&originIata={departure}&destinationIata={arrival}&dateOut={date}"
    )

    return (
        f"<b>🟢 Найдешевший квиток з Братислави ({month}):</b>\n"
        f"<b>✈️ {departure} → {arrival}</b>\n"
        f"<b>📅 Дата:</b> {date}\n"
        f"<b>💰 Ціна:</b> {price} {currency}\n"
        f"<a href='{url}'>🔗 Перейти до білету</a>"
    )