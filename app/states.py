from aiogram.fsm.state import StatesGroup, State

class SearchStates(StatesGroup):
    origin = State()          # výber mesta odletu
    month = State()           # výber mesiaca alebo „najbližších 7 dní“
    day = State()             # zadanie dňa (rok = 2025)
    price = State()           # výber cenového rozsahu
    return_range = State()    # výber rozsahu návratu
    processing = State()      # technický stav pri vyhľadávaní

class SubscribeStates(StatesGroup):
    waiting_for_route = State()
    waiting_for_transport = State()

class UnsubscribeStates(StatesGroup):
    waiting_for_subscription_id = State()
