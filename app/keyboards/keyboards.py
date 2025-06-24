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

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def month_keyboard():
    builder = InlineKeyboardBuilder()
    months = ["07", "08", "09", "10", "11", "12"]
    for m in months:
        builder.add(InlineKeyboardButton(text=f"📅 {m}", callback_data=m))
    builder.add(InlineKeyboardButton(text="🔙 Späť", callback_data="back"))
    builder.adjust(4)
    return builder.as_markup()

def price_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🌑 Do 30€", callback_data="to30"),
        InlineKeyboardButton(text="💰 30–50€", callback_data="30to50"),
        InlineKeyboardButton(text="🎯 Všetky", callback_data="all"),
        InlineKeyboardButton(text="📉 Najlacnejší z Bratislavy", callback_data="cheapest"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back")
    )
    builder.adjust(2)
    return builder.as_markup()


