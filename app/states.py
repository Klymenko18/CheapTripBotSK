from aiogram.fsm.state import StatesGroup, State

class SearchStates(StatesGroup):
    language = State()         # 🔹 нове: вибір мови на старті

    origin = State()           # вибір міста вильоту
    country_mode = State()     # всі напрямки чи конкретна країна
    country_select = State()   # вибір країни
    country_range = State()    # вибір періоду (1м / 1–3м / 3–6м / best6)
    country_return = State()   # ВИБІР інтервалу повернення для режиму "країна"

    country_city_mode = State()     # вибір "вся країна" чи "місто"
    country_city_select = State()   # вибір міста в межах країни


    month = State()            # (режим "всі") вибір місяця
    day = State()              # (режим "всі") день (рік = 2025)
    price = State()            # (режим "всі") ціновий діапазон
    return_range = State()     # (режим "всі") інтервал повернення
    processing = State()       # технічний стан


class SubscribeStates(StatesGroup):
    waiting_for_route = State()
    waiting_for_transport = State()


class UnsubscribeStates(StatesGroup):
    waiting_for_subscription_id = State()
