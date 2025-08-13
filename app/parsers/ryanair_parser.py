from datetime import datetime, timedelta
import requests
from typing import List, Dict, Any, Optional

from app.utils.cities import get_city_name
from app.utils.airports_country_map import airport_country  # мапа IATA -> ISO країни

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

def _price_bounds(price_cb: str) -> tuple[float, float] | None:
    # для загальної суми (odlet + návrat)
    if price_cb in ("p:cheapest", "p:all"):
        return None
    if price_cb == "p:<=50":
        return (0.0, 50.0)
    if price_cb == "p:50-80":
        return (50.0, 80.0)
    if price_cb == "p:80-100":
        return (80.0, 100.0)
    return (0.0, 9999.0)

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
    limit: int = 200,
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

    res = requests.get(url, params=params, headers=HEADERS, timeout=25)
    res.raise_for_status()
    data = res.json()
    return data.get("fares", []), int(data.get("total", 0))

def _fmt_rt(origin: str, to: str, out_date: str, back_date: str,
            out_price: float, back_price: float, currency: str = "EUR") -> str:
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

def _best_return(from_iata: str, to_iata: str, out_date: str,
                 min_days: int = 1, max_days: int = 14) -> tuple[Optional[str], float]:
    """Найдешевший зворотний квиток у вікні [min_days; max_days] від out_date."""
    dep = datetime.strptime(out_date, "%Y-%m-%d").date()
    date_from = (dep + timedelta(days=min_days)).strftime("%Y-%m-%d")
    date_to   = (dep + timedelta(days=max_days)).strftime("%Y-%m-%d")
    try:
        back_fares, _ = _one_way_fares(
            origin=to_iata,
            arrival=from_iata,
            date_from=date_from,
            date_to=date_to,
            market=_market_for(to_iata),
        )
    except Exception:
        return None, 9999.0
    if not back_fares:
        return None, 9999.0

    best_back = min(
        back_fares,
        key=lambda bf: float((bf.get("outbound", {}).get("price") or {}).get("value", 9999))
    )
    back_leg = best_back.get("outbound", {}) or {}
    back_date = (back_leg.get("departureDate") or "")[:10]
    back_price = float((back_leg.get("price") or {}).get("value", 9999))
    return back_date, back_price

# ---------------- all-countries (старий флоу) ----------------

def search_round_trip(origin: str, outbound_date: str, price_cb: str, return_cb: str) -> list[str]:
    price_bounds = _price_bounds(price_cb)     # None або (min,max) ДЛЯ TOTAL
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
        out = f.get("outbound", {}) or {}
        arr = (out.get("arrivalAirport", {}) or {}).get("iataCode")
        if not arr:
            continue

        try:
            out_price = float((out.get("price") or {}).get("value", 9999))
        except Exception:
            out_price = 9999.0

        back_date, back_price = _best_return(origin, arr, outbound_date, min_days=min_d, max_days=max_d)
        if not back_date:
            continue

        total = out_price + back_price
        candidates.append({
            "to": arr,
            "out_date": outbound_date,
            "back_date": back_date,
            "out_price": out_price,
            "back_price": back_price,
            "total": total,
        })

    if not candidates:
        return []

    candidates.sort(key=lambda x: x["total"])

    if price_cb == "p:cheapest":
        c = candidates[0]
        return [_fmt_rt(origin, c["to"], c["out_date"], c["back_date"], c["out_price"], c["back_price"])]

    if price_bounds is not None:
        low, high = price_bounds
        candidates = [c for c in candidates if low <= c["total"] <= high]

    if not candidates:
        return []

    return [
        _fmt_rt(origin, c["to"], c["out_date"], c["back_date"], c["out_price"], c["back_price"])
        for c in candidates[:30]
    ]

# ---------------- country mode + період + інтервал повернення ----------------

def _airport_country_from_api(outbound_obj: Dict[str, Any]) -> Optional[str]:
    """Код країни з відповіді API; якщо нема — з локальної мапи."""
    airport = outbound_obj.get("arrivalAirport", {}) or {}
    code = airport.get("countryCode") or (airport.get("country", {}) or {}).get("code")
    if code:
        return code.upper()
    iata = airport.get("iataCode")
    if iata:
        return airport_country.get(iata.upper())
    return None

def _window_dates(window_code: str) -> tuple[str, str]:
    """
    m:1    -> [today, today+30)
    m:1-3  -> [today+30, today+90)
    m:3-6  -> [today+90, today+180)
    m:best6 (default) -> [today, today+180)
    """
    today = datetime.now().date()
    if window_code == "m:1":
        start, end = today, today + timedelta(days=30)
    elif window_code == "m:1-3":
        start, end = today + timedelta(days=30), today + timedelta(days=90)
    elif window_code == "m:3-6":
        start, end = today + timedelta(days=90), today + timedelta(days=180)
    else:  # m:best6
        start, end = today, today + timedelta(days=180)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def search_round_trip_country_window(origin: str, country_code: str,
                                     window_code: str, return_cb: str,
                                     top_n: int = 3) -> List[str]:
    """
    1–3 найдешевші RT у міста обраної країни в заданому вікні дат
    та з обраним інтервалом повернення (r:1-3 / r:3-5 / r:5-10 / r:cheap14).
    """
    date_from, date_to = _window_dates(window_code)
    min_d, max_d = _range_bounds(return_cb)

    try:
        fares, _ = _one_way_fares(
            origin=origin,
            date_from=date_from,
            date_to=date_to,
            market=_market_for(origin),
            limit=200,
            offset=0,
        )
    except Exception:
        fares = []

    if not fares:
        return []

    targets: List[Dict[str, Any]] = []
    for f in fares:
        out = f.get("outbound", {}) or {}
        arr_iata = (out.get("arrivalAirport", {}) or {}).get("iataCode")
        if not arr_iata:
            continue

        cc = _airport_country_from_api(out)
        if not cc or cc.upper() != country_code.upper():
            continue

        out_date = (out.get("departureDate") or "")[:10]
        try:
            out_price = float((out.get("price") or {}).get("value", 9999))
        except Exception:
            out_price = 9999.0

        back_date, back_price = _best_return(origin, arr_iata, out_date, min_days=min_d, max_days=max_d)
        if not back_date:
            continue

        total = out_price + back_price
        targets.append({
            "to": arr_iata,
            "out_date": out_date,
            "back_date": back_date,
            "out_price": out_price,
            "back_price": back_price,
            "total": total,
        })

    if not targets:
        return []

    # один найкращий варіант на кожне місто
    best_per_city: Dict[str, Dict[str, Any]] = {}
    for c in targets:
        key = c["to"]
        if key not in best_per_city or c["total"] < best_per_city[key]["total"]:
            best_per_city[key] = c

    top = sorted(best_per_city.values(), key=lambda x: x["total"])[:max(1, min(top_n, 3))]

    return [
        _fmt_rt(origin, c["to"], c["out_date"], c["back_date"], c["out_price"], c["back_price"])
        for c in top
    ]

# збережено — тижневий пошук (one‑way)
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
        outbound = cheapest.get("outbound", {}) or {}
        arr = (outbound.get("arrivalAirport", {}) or {}).get("iataCode", "???")
        date = (outbound.get("departureDate") or "")[:10]
        price = float((outbound.get("price") or {}).get("value", 9999))

        booking_url = (
            "https://www.ryanair.com/gb/en/trip/flights/select?"
            f"adults=1&originIata={origin}&destinationIata={arr}&dateOut={date}"
        )
        messages.append(
            f"<b>✈️ {get_city_name(origin)} → {get_city_name(arr)}</b>\n"
            f"📅 {date}\n"
            f"💶 {price:.2f} EUR\n"
            f"<a href='{booking_url}'>🔗 Otvoriť</a>"
        )

    if not messages:
        return "❌ Nenašli sa žiadne lety na najbližší týždeň."

    cheapest_msg = min(
        messages,
        key=lambda s: float(s.split('💶 ')[1].split(' ')[0].replace(',', '.'))
    )
    return f"🟢 Najlacnejší let z najbližších 7 dní:\n{cheapest_msg}"
