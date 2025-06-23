from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import SearchStates
from app.keyboards.keyboards import month_keyboard

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Обери місяць для пошуку ✈️", reply_markup=month_keyboard())
    await state.set_state(SearchStates.month)  # 👈 ВАЖЛИВО!

@router.message(F.text == "/clear")
async def clear_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Історію очищено 🧼")
