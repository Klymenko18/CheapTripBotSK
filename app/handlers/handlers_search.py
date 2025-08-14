from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from calendar import monthrange

from app.states import SearchStates
from app.keyboards.keyboards import (
    language_keyboard,
    month_keyboard,
    price_keyboard,
    origin_keyboard,
    return_range_keyboard,
    country_mode_keyboard,
    country_select_keyboard,
    country_range_keyboard,
)
from app.parsers.ryanair_parser import (
    search_round_trip,
    get_cheapest_next_7_days,
    search_round_trip_country_window,  # парсер з return_cb
)
from app.utils.cities import get_city_name

router = Router()

# ------------ I18N (повідомлення) ------------
T = {
    "choose_lang": "Select language / Vyber jazyk / Wähle Sprache / Виберіть мову:",
    "unknown": {
        "en": "⚠️ Unknown choice. Try again.",
        "sk": "⚠️ Neznáma voľba. Skús znova.",
        "de": "⚠️ Unbekannte Auswahl. Bitte erneut versuchen.",
        "uk": "⚠️ Невідомий вибір. Спробуйте ще раз.",
    },
    "ask_origin": {
        "en": "From which city are we flying? 🌍",
        "sk": "Z ktorého mesta hľadáme? 🌍",
        "de": "Von welcher Stadt fliegen wir? 🌍",
        "uk": "З якого міста летимо? 🌍",
    },
    "country_or_all": {
        "en": "Search in all countries or a specific one? 🌐",
        "sk": "Hľadať vo všetkých krajinách, alebo len v jednej konkrétnej? 🌐",
        "de": "In allen Ländern oder nur in einem bestimmten suchen? 🌐",
        "uk": "Шукати по всіх країнах чи по конкретній? 🌐",
    },
    "pick_country": {
        "en": "Select country 🎯",
        "sk": "Vyber krajinu 🎯",
        "de": "Land auswählen 🎯",
        "uk": "Оберіть країну 🎯",
    },
    "pick_period": {
        "en": "Choose period ⏳",
        "sk": "Vyber obdobie vyhľadávania ⏳",
        "de": "Zeitraum wählen ⏳",
        "uk": "Оберіть період пошуку ⏳",
    },
    "pick_return": {
        "en": "Choose return ⏳",
        "sk": "Vyber si návrat ⏳",
        "de": "Rückflug wählen ⏳",
        "uk": "Виберіть повернення ⏳",
    },
    "ask_month": {
        "en": "Choose month ✈️",
        "sk": "Vyber si mesiac pre vyhľadávanie ✈️",
        "de": "Monat wählen ✈️",
        "uk": "Оберіть місяць ✈️",
    },
    "enter_day": {
        "en": "Enter <b>day</b> of departure in selected month (01–31).\nYear is fixed: <b>2025</b>.\n\nExample: <code>18</code>",
        "sk": "Zadaj <b>deň</b> odletu vo vybranom mesiaci (01–31).\nRok je pevne: <b>2025</b>.\n\nPríklad: <code>18</code>",
        "de": "Gib den <b>Tag</b> des Abflugs im gewählten Monat ein (01–31).\nJahr ist fix: <b>2025</b>.\n\nBeispiel: <code>18</code>",
        "uk": "Введіть <b>день</b> вильоту у вибраному місяці (01–31).\nРік фіксований: <b>2025</b>.\n\nПриклад: <code>18</code>",
    },
    "ask_price": {
        "en": "Choose price range 💶",
        "sk": "Vyber cenový rozsah 💶",
        "de": "Preisbereich wählen 💶",
        "uk": "Оберіть ціновий діапазон 💶",
    },
    "searching_all": {
        "en": "🔎 Searching round trips from {city}.\nOut: <b>{date}</b> • Return: <b>{ret}</b>\nPlease wait…",
        "sk": "🔎 Hľadám lety <b>tam a späť</b> z {city}.\nOdlet: <b>{date}</b> • Návrat: <b>{ret}</b>\nProsím, chvíľu počkaj…",
        "de": "🔎 Suche Hin- und Rückflüge ab {city}.\nHin: <b>{date}</b> • Rück: <b>{ret}</b>\nBitte warten…",
        "uk": "🔎 Шукаю перельоти <b>туди й назад</b> з {city}.\nВиліт: <b>{date}</b> • Повернення: <b>{ret}</b>\nЗачекайте…",
    },
    "searching_country": {
        "en": "🔎 Looking for 1–3 cheapest round trips from {city} to <b>{cc}</b> with return {ret}… Please wait.",
        "sk": "🔎 Hľadám 1–3 najlacnejšie lety tam a späť z {city} do krajiny <b>{cc}</b> s návratom {ret}… Prosím, chvíľu počkaj.",
        "de": "🔎 Suche 1–3 günstigste Hin- und Rückflüge ab {city} nach <b>{cc}</b> mit Rückflug {ret}… Bitte warten.",
        "uk": "🔎 Шукаю 1–3 найдешевші перельоти туди-назад з {city} до <b>{cc}</b> з поверненням {ret}… Зачекайте.",
    },
    "nothing": {
        "en": "❌ Nothing found for the selected parameters.",
        "sk": "❌ Nič sa nenašlo pre zadané parametre.",
        "de": "❌ Keine Ergebnisse für die gewählten Parameter.",
        "uk": "❌ Нічого не знайдено за обраними параметрами.",
    },
}

def _lng(data: dict) -> str:
    return (data or {}).get("language", "en")

async def send_batch(messages: list[str], send_func):
    if not messages:
        return
    batch_size = 8
    for i in range(0, len(messages), batch_size):
        text = "\n\n".join(messages[i:i + batch_size])
        await send_func(text)

# --------------- Start & language ----------------

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    # завжди починаємо з вибору мови
    await state.clear()
    await message.answer(T["choose_lang"], reply_markup=language_keyboard())
    await state.set_state(SearchStates.language)

@router.callback_query(SearchStates.language)
async def process_language(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if not callback.data.startswith("lang:"):
        return await callback.message.answer(T["unknown"]["en"])

    lang = callback.data.split(":", 1)[1]
    await state.update_data(language=lang)

    await callback.message.answer(T["ask_origin"][lang], reply_markup=origin_keyboard(lang))
    await state.set_state(SearchStates.origin)

# --------------- Flow ----------------

@router.callback_query(SearchStates.origin)
async def process_origin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        # назад до вибору мови
        return await cmd_start(callback.message, state)

    if ":" not in callback.data:
        await callback.message.answer(T["unknown"][lang])
        return await cmd_start(callback.message, state)

    origin = callback.data.split(":")[1]
    await state.update_data(origin=origin)

    await callback.message.answer(T["country_or_all"][lang], reply_markup=country_mode_keyboard(lang))
    await state.set_state(SearchStates.country_mode)

# --------- Country mode flow ---------

@router.callback_query(SearchStates.country_mode)
async def process_country_mode(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        return await cmd_start(callback.message, state)

    mode = callback.data.split(":", 1)[1] if ":" in callback.data else ""
    if mode == "pick":
        await callback.message.answer(T["pick_country"][lang], reply_markup=country_select_keyboard(lang))
        return await state.set_state(SearchStates.country_select)

    await callback.message.answer(T["ask_month"][lang], reply_markup=month_keyboard(lang))
    await state.set_state(SearchStates.month)

@router.callback_query(SearchStates.country_select)
async def process_country_select(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        # повертаємось до режиму вибору (all / pick)
        await callback.message.answer(T["country_or_all"][lang], reply_markup=country_mode_keyboard(lang))
        return await state.set_state(SearchStates.country_mode)

    if not callback.data.startswith("country:"):
        await callback.message.answer(T["unknown"][lang])
        return

    country_code = callback.data.split(":", 1)[1]
    await state.update_data(country_code=country_code)

    await callback.message.answer(T["pick_period"][lang], reply_markup=country_range_keyboard(lang))
    await state.set_state(SearchStates.country_range)

@router.callback_query(SearchStates.country_range)
async def process_country_range(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        await callback.message.answer(T["pick_country"][lang], reply_markup=country_select_keyboard(lang))
        return await state.set_state(SearchStates.country_select)

    await state.update_data(country_window=callback.data)  # m:1 / m:1-3 / m:3-6 / m:best6
    await callback.message.answer(T["pick_return"][lang], reply_markup=return_range_keyboard(lang))
    await state.set_state(SearchStates.country_return)

@router.callback_query(SearchStates.country_return)
async def process_country_return(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        await callback.message.answer(T["pick_period"][lang], reply_markup=country_range_keyboard(lang))
        return await state.set_state(SearchStates.country_range)

    return_cb = callback.data  # r:1-3 / r:3-5 / r:5-10 / r:cheap14
    origin = data.get("origin")
    country_code = data.get("country_code")
    window_code = data.get("country_window")

    city_name = get_city_name(origin)
    await callback.message.answer(
        T["searching_country"][lang].format(city=city_name, cc=country_code, ret=return_cb.replace("r:", "")),
    )

    results = search_round_trip_country_window(
        origin=origin,
        country_code=country_code,
        window_code=window_code,
        return_cb=return_cb,
        top_n=3,
    )

    if results:
        await send_batch(results, callback.message.answer)
    else:
        await callback.message.answer(T["nothing"][lang])

    return await cmd_start(callback.message, state)

# --------- Old flow (ALL countries) ---------

@router.callback_query(SearchStates.month)
async def process_month(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        return await cmd_start(callback.message, state)

    if callback.data == "week":
        origin = data.get("origin")
        if not origin:
            await callback.message.answer(T["ask_origin"][lang])
            return await cmd_start(callback.message, state)

        city_name = get_city_name(origin)
        await callback.message.answer(f"🔍 {city_name}: 7‑day cheapest scan…")
        result = get_cheapest_next_7_days(origin)
        await callback.message.answer(result)
        return await cmd_start(callback.message, state)

    month = callback.data
    await state.update_data(month=month)
    await callback.message.answer(T["enter_day"][lang])
    await state.set_state(SearchStates.day)

@router.message(SearchStates.day)
async def process_day(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    data = await state.get_data()
    lang = _lng(data)

    if not text.isdigit():
        return await message.answer("e.g. <code>05</code> or <code>18</code>")

    month = data.get("month")
    if not month:
        await message.answer(T["ask_month"][lang])
        return await state.set_state(SearchStates.month)

    day = int(text)
    _, last_day = monthrange(2025, int(month))
    if day < 1 or day > last_day:
        return await message.answer(f"Day must be in 1–{last_day}. Try again.")

    outbound_date = f"2025-{month}-{day:02d}"
    await state.update_data(outbound_date=outbound_date)

    await message.answer(T["ask_price"][lang], reply_markup=price_keyboard(lang))
    await state.set_state(SearchStates.price)

@router.callback_query(SearchStates.price)
async def process_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        return await cmd_start(callback.message, state)

    await state.update_data(price=callback.data)
    await callback.message.answer(T["pick_return"][lang], reply_markup=return_range_keyboard(lang))
    await state.set_state(SearchStates.return_range)

@router.callback_query(SearchStates.return_range)
async def process_return_range(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    lang = _lng(data)

    if callback.data == "back":
        return await cmd_start(callback.message, state)

    await state.update_data(return_range=callback.data)

    origin = data.get("origin")
    outbound_date = data.get("outbound_date")
    price_cb = data.get("price")
    range_cb = data.get("return_range")

    if not (origin and outbound_date and price_cb and range_cb):
        await callback.message.answer(T["unknown"][lang])
        return await cmd_start(callback.message, state)

    city_name = get_city_name(origin)
    await callback.message.answer(
        T["searching_all"][lang].format(city=city_name, date=outbound_date, ret=range_cb.replace("r:", "")),
    )

    results = search_round_trip(
        origin=origin,
        outbound_date=outbound_date,
        price_cb=price_cb,
        return_cb=range_cb,
    )

    if results:
        await send_batch(results, callback.message.answer)
    else:
        await callback.message.answer(T["nothing"][lang])

    await cmd_start(callback.message, state)
