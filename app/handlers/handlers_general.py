from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()

# ❌ Прибрано хендлер на /start, щоб не перебивав вибір мови

@router.message(F.text == "/clear")
async def clear_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("História bola vymazaná 🧼")
