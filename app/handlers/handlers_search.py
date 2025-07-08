from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from app.states import SearchStates
from app.keyboards.keyboards import (
    month_keyboard,
    price_keyboard,
    origin_keyboard,
    # return_day_keyboard — видалено
)
from app.parsers.ryanair_parser import search_tickets, get_cheapest_from_city, get_cheapest_next_7_days
from app.utils.cities import get_city_name

router = Router()

async def send_batch(messages: list[str], send_func):
    batch_size = 10
    for i in range(0, len(messages), batch_size):
        text = "\n\n".join(messages[i:i+batch_size])
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

    code = callback.data.split(":")[1]
    await state.update_data(origin=code)
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
        await callback.message.answer(f"🔍 Hľadáme najlacnejší let z najbližších 7 dní z {city_name}...")
        result = get_cheapest_next_7_days(origin)
        await callback.message.answer(result)
        return await cmd_start(callback.message, state)

    await state.update_data(month=callback.data)
    await callback.message.answer("Vyber cenový rozsah 💶", reply_markup=price_keyboard())
    await state.set_state(SearchStates.price)

@router.callback_query(SearchStates.price)
async def process_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "back":
        return await cmd_start(callback.message, state)

    await state.update_data(price=callback.data)

    if callback.data == "cheapest":
        data = await state.get_data()
        month = data.get("month")
        origin = data.get("origin", "BTS")

        if not month:
            await callback.message.answer("⚠️ Vyber najprv mesiac.")
            return await state.set_state(SearchStates.month)

        if not origin:
            await callback.message.answer("⚠️ Vyber najprv mesto.")
            return await state.set_state(SearchStates.origin)

        city_name = get_city_name(origin)
        await callback.message.answer(f"🔍 Hľadáme najlacnejší let z {city_name} v mesiaci {month}...")
        result = get_cheapest_from_city(month, origin)
        await callback.message.answer(result)
        return await cmd_start(callback.message, state)

    # 🔻 Одразу виконуємо пошук без вибору країни
    await callback.message.answer("🔍 Hľadáme lety, počkaj chvíľu...")
    data = await state.get_data()
    results = search_tickets(data)

    if results:
        await send_batch(results, callback.message.answer)
    else:
        await callback.message.answer("❌ Nič sa nenašlo v danom mesiaci.")

    await cmd_start(callback.message, state)
