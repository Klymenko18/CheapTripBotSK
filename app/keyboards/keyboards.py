from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def origin_keyboard():
    buttons = [
        InlineKeyboardButton(text="Братислава", callback_data="Братислава"),
        InlineKeyboardButton(text="Відень", callback_data="Відень"),
        InlineKeyboardButton(text="Будапешт", callback_data="Будапешт"),
        InlineKeyboardButton(text="Кошице", callback_data="Кошице")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons])

def month_keyboard():
    builder = InlineKeyboardBuilder()
    months = ["06", "07", "08", "09", "10", "11", "12"]
    for m in months:
        builder.add(InlineKeyboardButton(text=f"📅 {m}", callback_data=m))
    builder.adjust(4)
    return builder.as_markup()

def price_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🌑 До 30€", callback_data="30"),
        InlineKeyboardButton(text="💰 30–50€", callback_data="50"),
        InlineKeyboardButton(text="🎯 Усі", callback_data="all"),
        InlineKeyboardButton(text="📉 Найдешевший з Братислави", callback_data="cheapest")
    )
    builder.adjust(2)
    return builder.as_markup()

