from datetime import datetime, timedelta
import requests
from app.utils.cities import get_city_name

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def _market_for(origin: str) -> str:
    return {
        "BTS": "sk-sk",
        "KSC": "sk-sk",
        "VIE": "at-en",
        "BUD": "hu-hu",
    }.get(origin, "sk-sk")

def _price_bounds(price_cb: str) -> tuple[float, float]:
    if price_cb == "p:<=50":
        return 0, 50
    if price_cb == "p:50-80":
        return 50, 80
    return 0, 9999

def _range_bounds(return_cb: str) -> tuple[int, int]:
    if return_cb == "r:1-3":
        return 1, 3
    if return_cb == "r:3-5":
        return 3, 5
    if return_cb == "r:5-10":
        return 5, 10
    return 1, 14  # r:cheap14

def _one_way_fares(
    origin: str,
    date_from: str,
    date_to: str,
    arrival: str | None = None,
    market: str | None = None,
    limit: int = 64,
    offset: int = 0,
):
    url = "https://services-api.ryanair.com/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": origin,
        "outboundDepartureDateFrom": date_from,
        "outboundDepartureDateTo": date_to,
        "market": market or _market_for(origin),
        "language": "sk",
        "limit": limit,
        "offset": offset,
    }
    if arrival:
        params["arrivalAirportIataCode"] = arrival

    res = requests.get(url, params=params, headers=HEADERS, timeout=20)
    res.raise_for_status()
    data = res.json()
    return data.get("fares", []), data.get("total", 0)

def search_round_trip(origin: str, outbound_date: str, price_cb: str, return_cb: str) -> list[str]:
    min_price, max_price = _price_bounds(price_cb)
    min_d, max_d = _range_bounds(return_cb)

    fares, _ = _one_way_fares(
        origin=origin,
        date_from=outbound_date,
        date_to=outbound_date,
        market=_market_for(origin),
    )
    if not fares:
        return []

    candidates = []
    for f in fares:
        out = f.get("outbound", {})
        arr = out.get("arrivalAirport", {}).get("iataCode")
        if not arr:
            continue
        out_price = (out.get("price") or {}).get("value", 9999)
        out_currency = (out.get("price") or {}).get("currencyCode", "EUR")

        if not (min_price <= float(out_price) <= max_price):
            continue

        dep = datetime.strptime(outbound_date, "%Y-%m-%d").date()
        date_from = (dep + timedelta(days=min_d)).strftime("%Y-%m-%d")
        date_to = (dep + timedelta(days=max_d)).strftime("%Y-%m-%d")

        try:
            back_fares, _ = _one_way_fares(
                origin=arr,
                arrival=origin,
                date_from=date_from,
                date_to=date_to,
                market=_market_for(arr),
            )
        except Exception:
            continue

        if not back_fares:
            continue

        best_back = min(
            back_fares,
            key=lambda bf: (bf.get("outbound", {}).get("price") or {}).get("value", 9999)
        )
        back_leg = best_back.get("outbound", {})
        back_date = (back_leg.get("departureDate") or "")[:10]
        back_price = (back_leg.get("price") or {}).get("value", 9999)
        back_currency = (back_leg.get("price") or {}).get("currencyCode", "EUR")

        total_price = float(out_price) + float(back_price)
        candidates.append({
            "to": arr,
            "out_date": outbound_date,
            "back_date": back_date,
            "out_price": out_price,
            "back_price": back_price,
            "currency": out_currency or back_currency or "EUR",
            "total": total_price,
        })

    candidates.sort(key=lambda x: x["total"])
    results = []
    for c in candidates[:30]:
        booking_url = (
            "https://www.ryanair.com/gb/en/trip/flights/select?"
            "adults=1&teens=0&children=0&infants=0&isConnectedFlight=false"
            f"&isReturn=true&discount=0&originIata={origin}&destinationIata={c['to']}"
            f"&dateOut={c['out_date']}&dateIn={c['back_date']}"
        )
        results.append(
            f"<b>✈️ {get_city_name(origin)} → {get_city_name(c['to'])}</b>\n"
            f"📅 <b>Odlet:</b> {c['out_date']} • <b>Návrat:</b> {c['back_date']}\n"
            f"💶 <b>Odlet:</b> {c['out_price']} {c['currency']}  |  "
            f"<b>Návrat:</b> {c['back_price']} {c['currency']}\n"
            f"🟢 <b>Spolu:</b> {c['total']:.2f} {c['currency']}\n"
            f"<a href='{booking_url}'>🔗 Otvoriť v Ryanair</a>"
        )

    return results

def get_cheapest_next_7_days(origin="BTS"):
    today = datetime.now().date()
    messages = []

    for i in range(7):
        day = today + timedelta(days=i)
        try:
            fares, _ = _one_way_fares(
                origin=origin,
                date_from=day.strftime("%Y-%m-%d"),
                date_to=day.strftime("%Y-%m-%d"),
            )
        except Exception:
            continue

        if not fares:
            continue

        cheapest = min(
            fares,
            key=lambda f: (f.get("outbound", {}).get("price") or {}).get("value", 9999)
        )
        outbound = cheapest.get("outbound", {})
        arr = outbound.get("arrivalAirport", {}).get("iataCode", "???")
        date = outbound.get("departureDate", "")[:10]
        price = (outbound.get("price") or {}).get("value", 9999)
        currency = (outbound.get("price") or {}).get("currencyCode", "EUR")

        booking_url = (
            "https://www.ryanair.com/gb/en/trip/flights/select?"
            f"adults=1&originIata={origin}&destinationIata={arr}&dateOut={date}"
        )
        messages.append(
            f"<b>✈️ {get_city_name(origin)} → {get_city_name(arr)}</b>\n"
            f"📅 {date}\n"
            f"💶 {price} {currency}\n"
            f"<a href='{booking_url}'>🔗 Otvoriť</a>"
        )

    if not messages:
        return "❌ Nenašli sa žiadne lety na najbližší týždeň."

    cheapest_msg = min(
        messages,
        key=lambda s: float(s.split('💶 ')[1].split(' ')[0].replace(',', '.'))
    )
    return f"🟢 Najlacnejší let z najbližších 7 dní:\n{cheapest_msg}"
