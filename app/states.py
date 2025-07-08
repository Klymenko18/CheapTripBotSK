from aiogram.fsm.state import StatesGroup, State

class SearchStates(StatesGroup):
    origin = State()
    month = State()
    price = State()
    country = State()

class SubscribeStates(StatesGroup):
    waiting_for_route = State()
    waiting_for_transport = State()

class UnsubscribeStates(StatesGroup):
    waiting_for_subscription_id = State()
