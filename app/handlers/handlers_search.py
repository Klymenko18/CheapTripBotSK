from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from app.states import SearchStates
from app.keyboards.keyboards import month_keyboard, price_keyboard
from app.parsers.ryanair_parser import (
    search_tickets,
    get_cheapest_from_bratislava,
    get_cheapest_next_7_days,
)

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)


@router.callback_query(SearchStates.month)
async def month_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "back":
        await cmd_start(callback.message, state)
        return

    await state.update_data(month=callback.data)
    await callback.message.answer("Vyber cenový rozsah 💶", reply_markup=price_keyboard())
    await state.set_state(SearchStates.price)


@router.callback_query(SearchStates.price)
async def price_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    month = data.get("month")
    price_cb = callback.data

    if price_cb == "back":
        await callback.message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
        await state.set_state(SearchStates.month)
        return

    if month == "week":
        if price_cb == "cheapest":
            await callback.message.answer("🔍 Hľadáme najlacnejší let na najbližších 7 dní...")
            result = get_cheapest_next_7_days()
            await callback.message.answer(result)
        else:
            min_price = 0
            max_price = 999
            if price_cb == "30":
                max_price = 30
            elif price_cb == "50":
                min_price = 30
                max_price = 50

            await callback.message.answer(f"🔎 Hľadáme lety na najbližších 7 dní medzi {min_price}–{max_price}€...")
            today = datetime.now().date()
            results = []

            for i in range(7):
                day = today + timedelta(days=i)
                m = str(day.month).zfill(2)
                d_results = search_tickets(m, max_price, min_price)
                for r in d_results:
                    if f"{day.year}-{m}-{str(day.day).zfill(2)}" in r:
                        results.append(r)

            if results:
                for r in results:
                    await callback.message.answer(r)
            else:
                await callback.message.answer("❌ Nenašli sa žiadne lety na najbližší týždeň.")

        await callback.message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
        await state.set_state(SearchStates.month)
        return

    if price_cb == "cheapest":
        await callback.message.answer(f"🔍 Hľadáme najlacnejšiu letenku z Bratislavy v mesiaci {month}...")
        result = get_cheapest_from_bratislava(month)
        await callback.message.answer(result)
        await callback.message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
        await state.set_state(SearchStates.month)
        return

    try:
        min_price = 0
        max_price = 999
        if price_cb == "30":
            max_price = 30
        elif price_cb == "50":
            min_price = 30
            max_price = 50

        await callback.message.answer(f"🔎 Hľadáme lety v {month}. mesiaci medzi {min_price}–{max_price}€...")
        results = search_tickets(month, max_price, min_price)
        for text in results:
            await callback.message.answer(text)

    except Exception as e:
        await callback.message.answer(f"⚠️ Chyba: {str(e)}")

    await callback.message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)
