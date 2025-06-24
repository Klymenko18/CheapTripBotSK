from aiogram.fsm.state import State, StatesGroup

class SearchStates(StatesGroup):
    month = State()
    price = State()
    week = State()