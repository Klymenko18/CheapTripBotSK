from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from calendar import monthrange

from app.states import SearchStates
from app.keyboards.keyboards import (
    month_keyboard,
    price_keyboard,
    origin_keyboard,
    return_range_keyboard,
)
from app.parsers.ryanair_parser import (
    search_round_trip,
    get_cheapest_next_7_days,
)
from app.utils.cities import get_city_name

router = Router()

async def send_batch(messages: list[str], send_func):
    if not messages:
        return
    batch_size = 8
    for i in range(0, len(messages), batch_size):
        text = "\n\n".join(messages[i:i + batch_size])
        await send_func(text)

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Z ktorého mesta hľadáme? 🌍", reply_markup=origin_keyboard())
    await state.set_state(SearchStates.origin)

@router.callback_query(SearchStates.origin)
async def process_origin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "back":
        return await cmd_start(callback.message, state)

    if ":" not in callback.data:
        await callback.message.answer("⚠️ Neznáma voľba. Skús znova.")
        return await cmd_start(callback.message, state)

    origin = callback.data.split(":")[1]
    await state.update_data(origin=origin)
    await callback.message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)

@router.callback_query(SearchStates.month)
async def process_month(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "back":
        return await cmd_start(callback.message, state)

    if callback.data == "week":
        data = await state.get_data()
        origin = data.get("origin")
        if not origin:
            await callback.message.answer("⚠️ Najprv vyber mesto odletu.")
            return await cmd_start(callback.message, state)

        city_name = get_city_name(origin)
        await callback.message.answer(f"🔍 Hľadáme najlacnejší let z najbližších 7 dní z {city_name}…")
        result = get_cheapest_next_7_days(origin)
        await callback.message.answer(result)
        return await cmd_start(callback.message, state)

    # ulož mesiac a požiadaj o DEŇ (rok je pevne 2025)
    month = callback.data  # '07'..'12'
    await state.update_data(month=month)
    await callback.message.answer(
        "Zadaj <b>deň</b> odletu vo vybranom mesiaci (01–31).\n"
        "Rok je pevne: <b>2025</b>.\n\n"
        "Príklad: <code>18</code>"
    )
    await state.set_state(SearchStates.day)

@router.message(SearchStates.day)
async def process_day(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if not text.isdigit():
        return await message.answer("Zadaj číslo dňa, napr.: <code>05</code> alebo <code>18</code>.")

    data = await state.get_data()
    month = data.get("month")
    if not month:
        await message.answer("⚠️ Najprv vyber mesiac.")
        return await state.set_state(SearchStates.month)

    day = int(text)
    _, last_day = monthrange(2025, int(month))
    if day < 1 or day > last_day:
        return await message.answer(f"V tomto mesiaci musí byť deň v rozsahu 1–{last_day}. Zadaj znova.")

    outbound_date = f"2025-{month}-{day:02d}"
    await state.update_data(outbound_date=outbound_date)

    await message.answer("Vyber cenový rozsah 💶", reply_markup=price_keyboard())
    await state.set_state(SearchStates.price)

@router.callback_query(SearchStates.price)
async def process_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "back":
        return await cmd_start(callback.message, state)

    await state.update_data(price=callback.data)  # p:<=50 / p:50-80 / p:all

    # výber rozsahu návratu
    await callback.message.answer("Vyber si návrat ⏳", reply_markup=return_range_keyboard())
    await state.set_state(SearchStates.return_range)

@router.callback_query(SearchStates.return_range)
async def process_return_range(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "back":
        return await cmd_start(callback.message, state)

    await state.update_data(return_range=callback.data)  # r:1-3 / r:3-5 / r:5-10 / r:cheap14

    data = await state.get_data()
    origin = data.get("origin")
    outbound_date = data.get("outbound_date")
    price_cb = data.get("price")
    range_cb = data.get("return_range")

    if not (origin and outbound_date and price_cb and range_cb):
        await callback.message.answer("⚠️ Chýbajú údaje na vyhľadávanie. Začnime odznova.")
        return await cmd_start(callback.message, state)

    city_name = get_city_name(origin)
    await callback.message.answer(
        f"🔎 Hľadám lety <b>tam a späť</b> z {city_name}.\n"
        f"Odlet: <b>{outbound_date}</b> • Návrat: <b>{range_cb.replace('r:','')}</b>\n"
        f"Prosím, chvíľu počkaj…"
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
        await callback.message.answer("❌ Nič sa nenašlo pre zadané parametre.")

    await cmd_start(callback.message, state)
