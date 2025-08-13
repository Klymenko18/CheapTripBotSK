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
    # p:<=50 / p:50-80 / p:80-100 / p:cheapest / p:all
    if price_cb == "p:<=50":
        return 0, 50
    if price_cb == "p:50-80":
        return 50, 80
    if price_cb == "p:80-100":
        return 80, 100
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

def _fmt_rt(origin: str, to: str, out_date: str, back_date: str,
            out_price: float, back_price: float, currency: str) -> str:
    """Formát výstupu: Odlet — dátum — cena; Návrat — dátum — cena; Spolu."""
    booking_url = (
        "https://www.ryanair.com/gb/en/trip/flights/select?"
        "adults=1&teens=0&children=0&infants=0&isConnectedFlight=false"
        f"&isReturn=true&discount=0&originIata={origin}&destinationIata={to}"
        f"&dateOut={out_date}&dateIn={back_date}"
    )
    total = float(out_price) + float(back_price)
    return (
        f"<b>✈️ {get_city_name(origin)} → {get_city_name(to)}</b>\n"
        f"🛫 <b>Odlet</b> — {out_date} — <b>{float(out_price):.2f} {currency}</b>\n"
        f"🛬 <b>Návrat</b> — {back_date} — <b>{float(back_price):.2f} {currency}</b>\n"
        f"🟢 <b>Spolu:</b> {total:.2f} {currency}\n"
        f"<a href='{booking_url}'>🔗 Otvoriť v Ryanair</a>"
    )

def search_round_trip(origin: str, outbound_date: str, price_cb: str, return_cb: str) -> list[str]:
    """
    Hľadá RT:
      - pre všetky destinácie v daný deň nájde najlacnejšie späť v zadanom okne
      - ak price_cb == 'p:cheapest' → vráti iba JEDNU najlacnejšiu dvojicu podľa sumy
      - inak vráti zoradený zoznam (najlacnejšie navrchu)
    """
    min_price, max_price = _price_bounds(price_cb)
    min_d, max_d = _range_bounds(return_cb)
    limit_outbound = price_cb not in ("p:all", "p:cheapest")

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

        out_price = float((out.get("price") or {}).get("value", 9999))
        out_currency = (out.get("price") or {}).get("currencyCode", "EUR") or "EUR"

        if limit_outbound and not (min_price <= out_price <= max_price):
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
            key=lambda bf: float((bf.get("outbound", {}).get("price") or {}).get("value", 9999))
        )
        back_leg = best_back.get("outbound", {})
        back_date = (back_leg.get("departureDate") or "")[:10]
        back_price = float((back_leg.get("price") or {}).get("value", 9999))
        currency = out_currency or (back_leg.get("price") or {}).get("currencyCode", "EUR") or "EUR"

        candidates.append({
            "to": arr,
            "out_date": outbound_date,
            "back_date": back_date,
            "out_price": out_price,
            "back_price": back_price,
            "currency": currency,
            "total": out_price + back_price,
        })

    if not candidates:
        return []

    candidates.sort(key=lambda x: x["total"])

    if price_cb == "p:cheapest":
        c = candidates[0]
        return [_fmt_rt(origin, c["to"], c["out_date"], c["back_date"],
                        c["out_price"], c["back_price"], c["currency"])]

    results = []
    for c in candidates[:30]:
        results.append(_fmt_rt(origin, c["to"], c["out_date"], c["back_date"],
                               c["out_price"], c["back_price"], c["currency"]))
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
            key=lambda f: float((f.get("outbound", {}).get("price") or {}).get("value", 9999))
        )
        outbound = cheapest.get("outbound", {})
        arr = outbound.get("arrivalAirport", {}).get("iataCode", "???")
        date = outbound.get("departureDate", "")[:10]
        price = float((outbound.get("price") or {}).get("value", 9999))
        currency = (outbound.get("price") or {}).get("currencyCode", "EUR") or "EUR"

        booking_url = (
            "https://www.ryanair.com/gb/en/trip/flights/select?"
            f"adults=1&originIata={origin}&destinationIata={arr}&dateOut={date}"
        )
        messages.append(
            f"<b>✈️ {get_city_name(origin)} → {get_city_name(arr)}</b>\n"
            f"📅 {date}\n"
            f"💶 {price:.2f} {currency}\n"
            f"<a href='{booking_url}'>🔗 Otvoriť</a>"
        )

    if not messages:
        return "❌ Nenašli sa žiadne lety na najbližší týždeň."

    cheapest_msg = min(
        messages,
        key=lambda s: float(s.split('💶 ')[1].split(' ')[0].replace(',', '.'))
    )
    return f"🟢 Najlacnejší let z najbližších 7 dní:\n{cheapest_msg}"
