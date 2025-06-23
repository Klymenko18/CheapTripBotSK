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
    await message.answer("Обери місяць для пошуку ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)

@router.callback_query(SearchStates.month)
async def month_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(month=callback.data)
    await callback.message.answer("Обери діапазон цін 💶", reply_markup=price_keyboard())
    await state.set_state(SearchStates.price)

@router.callback_query(SearchStates.price)
async def price_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    month = data.get("month")
    price_cb = callback.data

    if price_cb == "cheapest":
        await callback.message.answer(f"🔍 Шукаємо найдешевший квиток з Братислави у {month} місяці...")
        result = get_cheapest_from_bratislava(month)
        if result:
            await callback.message.answer(result)
        else:
            await callback.message.answer("❌ Нічого не знайдено.")
        await state.clear()
        return

    try:
        price = 999 if price_cb == "all" else int(price_cb)
    except ValueError:
        await callback.message.answer("⚠️ Помилка у ціні.")
        await state.clear()
        return

    await callback.message.answer(f"🔍 Шукаємо квитки в {month} місяці до {price}€...")
    results = search_tickets(month, price)  # міста не передаємо

    if results:
        for r in results:
            await callback.message.answer(r)
    else:
        await callback.message.answer("❌ Квитків не знайдено.")

    await state.clear()
