from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def month_keyboard():
    builder = InlineKeyboardBuilder()
    months = {
        "07": "📅 7 Júl",
        "08": "📅 8 August",
        "09": "📅 9 September",
        "10": "📅 10 Október",
        "11": "📅 11 November",
        "12": "📅 12 December",
    }
    for code, label in months.items():
        builder.add(InlineKeyboardButton(text=label, callback_data=code))
    builder.add(
        InlineKeyboardButton(text="🗓️ Najbližších 7 dní", callback_data="week"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back"),
    )
    builder.adjust(3)
    return builder.as_markup()

def price_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="💶 Do 50€", callback_data="p:<=50"),
        InlineKeyboardButton(text="💶 50–80€", callback_data="p:50-80"),
        InlineKeyboardButton(text="🌟 Všetky", callback_data="p:all"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back"),
    )
    builder.adjust(2)
    return builder.as_markup()

def origin_keyboard():
    cities = [
        ("🇸🇰 Bratislava", "BTS"),
        ("🇸🇰 Košice", "KSC"),
        ("🇦🇹 Viedeň", "VIE"),
    ]
    builder = InlineKeyboardBuilder()
    for name, code in cities:
        builder.add(InlineKeyboardButton(text=name, callback_data=f"origin:{code}"))
    builder.add(InlineKeyboardButton(text="🔙 Späť", callback_data="back"))
    builder.adjust(2)
    return builder.as_markup()

def return_range_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="↩️ O 1–3 dni", callback_data="r:1-3"),
        InlineKeyboardButton(text="↩️ O 3–5 dní", callback_data="r:3-5"),
        InlineKeyboardButton(text="↩️ O 5–10 dní", callback_data="r:5-10"),
        InlineKeyboardButton(text="🟢 Najlacnejšie (do 2 týždňov)", callback_data="r:cheap14"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back"),
    )
    builder.adjust(1)
    return builder.as_markup()
