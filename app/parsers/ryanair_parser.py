import requests
from datetime import datetime


def search_tickets(month: str, max_price: int):
    year = datetime.now().year
    results = []
    offset = 0
    limit = 64

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    while True:
        url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
        params = {
            "departureAirportIataCode": "BTS",
            "outboundDepartureDateFrom": f"{year}-{month}-01",
            "outboundDepartureDateTo": f"{year}-{month}-31",
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
            results.append(f"⚠️ Помилка при запиті: {str(e)}")
            break

        if not fares:
            break

        for fare in fares:
            outbound = fare.get("outbound", {})
            price_info = outbound.get("price", {})
            price = price_info.get("value", 999)
            currency = price_info.get("currencyCode", "EUR")

            if price > max_price:
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
                f"<b>📅 Дата:</b> {date}\n"
                f"<b>💰 Ціна:</b> {price} {currency}\n"
                f"<a href='{booking_url}'>🔗 Перейти до білету</a>"
            )
            results.append(text)

        total = data.get("total", 0)
        offset += limit
        if offset >= total:
            break

    if not results:
        results.append("❌ Квитків не знайдено на цей місяць.")

    return results


def get_cheapest_from_bratislava(month: str):
    year = datetime.now().year
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": "BTS",
        "outboundDepartureDateFrom": f"{year}-{month}-01",
        "outboundDepartureDateTo": f"{year}-{month}-31",
        "market": "sk-sk",
        "language": "sk",
        "limit": 64,
        "offset": 0
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
    except Exception:
        return "⚠️ Не вдалося отримати відповідь від сервера."

    fares = data.get("fares", [])
    if not fares:
        return "❌ Квитків не знайдено."

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
        f"<b>🟢 Найдешевший квиток з Братислави ({month}):</b>\n"
        f"<b>✈️ {departure} → {arrival}</b>\n"
        f"<b>📅 Дата:</b> {date}\n"
        f"<b>💰 Ціна:</b> {price} {currency}\n"
        f"<a href='{booking_url}'>🔗 Перейти до білету</a>"
    )
