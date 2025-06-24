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
    await message.answer("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)

@router.callback_query(SearchStates.month)
async def month_selected(callback: CallbackQuery, state: FSMContext):
    if callback.data == "back":
        await state.clear()
        await callback.message.edit_text("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
        return

    await callback.answer()
    await state.update_data(month=callback.data)
    await callback.message.edit_text("Vyber si cenový rozsah 💶", reply_markup=price_keyboard())
    await state.set_state(SearchStates.price)

@router.callback_query(SearchStates.price)
async def price_selected(callback: CallbackQuery, state: FSMContext):
    if callback.data == "back":
        await callback.message.edit_text("Vyber si mesiac pre vyhľadávanie ✈️", reply_markup=month_keyboard())
        await state.set_state(SearchStates.month)
        return

    await callback.answer()
    data = await state.get_data()
    month = data.get("month")
    price_cb = callback.data

    if price_cb == "cheapest":
        await callback.message.edit_text(f"🔍 Hľadáme najlacnejšiu letenku z Bratislavy v mesiaci {month}...")
        result = get_cheapest_from_bratislava(month)
        await callback.message.answer(result)
        await callback.message.answer("⬅️ Späť", reply_markup=month_keyboard())
        await state.set_state(SearchStates.month)
        return

    try:
        if price_cb == "all":
            min_price, max_price = 0, 999
        elif price_cb == "30":
            min_price, max_price = 0, 30
        elif price_cb == "50":
            min_price, max_price = 30, 50
        else:
            raise ValueError
    except ValueError:
        await callback.message.edit_text("⚠️ Neplatná cena.")
        await state.clear()
        return

    await callback.message.edit_text(f"🔍 Hľadáme letenky v mesiaci {month} za {min_price}–{max_price} €...")
    results = search_tickets(month, max_price, min_price)

    if results:
        for r in results:
            await callback.message.answer(r, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await callback.message.answer("❌ Nenašli sa žiadne letenky.")

    await callback.message.answer("⬅️ Späť", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)
