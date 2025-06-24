from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states import SearchStates
from app.keyboards.keyboards import month_keyboard, price_keyboard
from app.parsers.ryanair_parser import search_tickets, get_cheapest_from_bratislava

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Vyber mesiac na hľadanie ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)

@router.callback_query(SearchStates.month)
async def month_selected(callback: CallbackQuery, state: FSMContext):
    if callback.data == "back":
        await cmd_start(callback.message, state)
        return

    await callback.answer()
    await state.update_data(month=callback.data)
    await callback.message.answer("Vyber cenový rozsah 💶", reply_markup=price_keyboard())
    await state.set_state(SearchStates.price)

@router.callback_query(SearchStates.price)
async def price_selected(callback: CallbackQuery, state: FSMContext):
    if callback.data == "back":
        await callback.message.answer("Vyber mesiac znova ✈️", reply_markup=month_keyboard())
        await state.set_state(SearchStates.month)
        return

    await callback.answer()
    data = await state.get_data()
    month = data.get("month")
    cb = callback.data

    if cb == "cheapest":
        await callback.message.answer(f"🔍 Hľadáme najlacnejší let z Bratislavy v mesiaci {month}...")
        result = get_cheapest_from_bratislava(month)
        await callback.message.answer(result or "❌ Nič sa nenašlo.")
        await state.clear()
        return

    try:
        min_price = 0
        max_price = 999
        if cb == "to30":
            max_price = 30
        elif cb == "30to50":
            min_price = 30
            max_price = 50
    except ValueError:
        await callback.message.answer("⚠️ Chyba v cene.")
        await state.clear()
        return

    await callback.message.answer(f"🔍 Hľadáme lety v {month}. mesiaci medzi {min_price}–{max_price}€...")
    results = search_tickets(month, max_price, min_price)

    if results:
        for r in results:
            await callback.message.answer(r)
    else:
        await callback.message.answer("❌ Lety sa nenašli.")

    await state.clear()
