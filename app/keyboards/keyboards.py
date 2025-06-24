from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def origin_keyboard():
    buttons = [
        InlineKeyboardButton(text="Bratislava", callback_data="Братислава"),
        InlineKeyboardButton(text="Viedeň", callback_data="Відень"),
        InlineKeyboardButton(text="Budapešť", callback_data="Будапешт"),
        InlineKeyboardButton(text="Košice", callback_data="Кошице"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons])


def month_keyboard():
    builder = InlineKeyboardBuilder()
    months = ["07", "08", "09", "10", "11", "12"]  # 06 прибрано
    for m in months:
        builder.add(InlineKeyboardButton(text=f"📅 {m}", callback_data=m))
    builder.add(InlineKeyboardButton(text="🔙 Späť", callback_data="back"))
    builder.adjust(3)
    return builder.as_markup()


def price_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🌑 Do 30€", callback_data="30"),
        InlineKeyboardButton(text="💰 30–50€", callback_data="50"),
        InlineKeyboardButton(text="🎯 Všetky", callback_data="all"),
        InlineKeyboardButton(text="📉 Najlacnejší z Bratislavy", callback_data="cheapest"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back")
    )
    builder.adjust(2)
    return builder.as_markup()
