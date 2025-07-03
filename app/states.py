from aiogram.fsm.state import StatesGroup, State

class SearchStates(StatesGroup):
    origin = State()
    month = State()
    price = State()
    country = State()
    return_date = State()  # залишено, якщо ще буде використовуватись для ±3 днів

class SubscribeStates(StatesGroup):
    waiting_for_route = State()
    waiting_for_transport = State()

class UnsubscribeStates(StatesGroup):
    waiting_for_subscription_id = State()
