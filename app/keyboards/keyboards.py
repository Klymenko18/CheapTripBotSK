from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from datetime import datetime
from calendar import monthrange

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
        InlineKeyboardButton(text="🔙 Späť", callback_data="back")
    )
    builder.adjust(3)
    return builder.as_markup()

def price_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🌑 Do 30€", callback_data="30"),
        InlineKeyboardButton(text="💰 30–50€", callback_data="50"),
        InlineKeyboardButton(text="🌟 Všetky", callback_data="all"),
        InlineKeyboardButton(text="📉 Najlacnejší", callback_data="cheapest"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back")
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

def country_keyboard():
    countries = [
        ("🇮🇹 Taliansko", "IT"),
        ("🇪🇸 Španielsko", "ES"),
        ("🇬🇷 Grécko", "GR"),
        ("🇫🇷 Francúzsko", "FR"),
        ("🇩🇪 Nemecko", "DE"),
        ("🇵🇹 Portugalsko", "PT"),
        ("🇧🇪 Belgicko", "BE"),
        ("🇳🇱 Holandsko", "NL"),
        ("🇨🇿 Česko", "CZ"),
        ("🇦🇹 Rakúsko", "AT"),
        ("🇭🇷 Chorvátsko", "HR"),
        ("🇭🇺 Maďarsko", "HU"),
        ("🇸🇰 Slovensko", "SK"),
        ("🇬🇧 Veľká Británia", "GB"),
        ("🇳🇴 Nórsko", "NO"),
        ("🇸🇪 Švédsko", "SE"),
        ("🇩🇰 Dánsko", "DK"),
        ("🇵🇱 Poľsko", "PL"),
    ]
    builder = InlineKeyboardBuilder()
    for label, code in countries:
        builder.add(InlineKeyboardButton(text=label, callback_data=f"country:{code}"))
    builder.add(
        InlineKeyboardButton(text="🌍 Všetky krajiny", callback_data="country:ALL"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back")
    )
    builder.adjust(2)
    return builder.as_markup()

def return_day_keyboard(month: str):
    builder = InlineKeyboardBuilder()
    year = datetime.now().year
    try:
        month_int = int(month)
        _, last_day = monthrange(year, month_int)
    except ValueError:
        return builder.as_markup()

    for day in range(1, last_day + 1):
        day_str = str(day).zfill(2)
        builder.add(InlineKeyboardButton(text=day_str, callback_data=f"returnday:{day_str}"))
    builder.add(InlineKeyboardButton(text="🔙 Späť", callback_data="back"))
    builder.adjust(7)
    return builder.as_markup()
