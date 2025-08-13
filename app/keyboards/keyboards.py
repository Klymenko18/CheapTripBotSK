from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def month_keyboard():
    builder = InlineKeyboardBuilder()
    months = {
        "08": "📅 8 August",
        "09": "📅 9 September",
        "10": "📅 10 Október",
        "11": "📅 11 November",
        "12": "📅 12 December",
    }
    for code, label in months.items():
        builder.add(InlineKeyboardButton(text=label, callback_data=code))
    builder.add(InlineKeyboardButton(text="🔙 Späť", callback_data="back"))
    builder.adjust(3)
    return builder.as_markup()

def price_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="💶 Do 50€", callback_data="p:<=50"),
        InlineKeyboardButton(text="💶 50–80€", callback_data="p:50-80"),
        InlineKeyboardButton(text="💶 80–100€", callback_data="p:80-100"),
        InlineKeyboardButton(text="🟢 Najlacnejšie", callback_data="p:cheapest"),
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

# --- режим "країна" ---

def country_mode_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🌍 Všetky krajiny", callback_data="country_mode:all"),
        InlineKeyboardButton(text="🎯 Konkrétna krajina", callback_data="country_mode:pick"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back"),
    )
    builder.adjust(1)
    return builder.as_markup()

def country_select_keyboard():
    # Європейські напрямки Ryanair (ISO‑2 код країни → напис на кнопці)
    # Джерела переліку див. коментар нижче.
    countries = [
        ("IT", "🇮🇹 Italy"), ("ES", "🇪🇸 Spain"), ("FR", "🇫🇷 France"),
        ("PT", "🇵🇹 Portugal"), ("NL", "🇳🇱 Netherlands"), ("DE", "🇩🇪 Germany"),
        ("PL", "🇵🇱 Poland"), ("AT", "🇦🇹 Austria"), ("BE", "🇧🇪 Belgium"),
        ("IE", "🇮🇪 Ireland"), ("GB", "🇬🇧 United Kingdom"), ("CH", "🇨🇭 Switzerland"),
        ("SE", "🇸🇪 Sweden"), ("NO", "🇳🇴 Norway"), ("DK", "🇩🇰 Denmark"),
        ("FI", "🇫🇮 Finland"), ("EE", "🇪🇪 Estonia"), ("LV", "🇱🇻 Latvia"),
        ("LT", "🇱🇹 Lithuania"), ("LU", "🇱🇺 Luxembourg"), ("MT", "🇲🇹 Malta"),
        ("GR", "🇬🇷 Greece"), ("CY", "🇨🇾 Cyprus"), ("HR", "🇭🇷 Croatia"),
        ("SI", "🇸🇮 Slovenia"),  # якщо з’явиться — просто лишається; якщо ні — кнопку можна сховати
        ("CZ", "🇨🇿 Czech Republic"),
        ("HU", "🇭🇺 Hungary"), ("RO", "🇷🇴 Romania"), ("BG", "🇧🇬 Bulgaria"),
        ("AL", "🇦🇱 Albania"), ("BA", "🇧🇦 Bosnia and Herzegovina"),
        ("ME", "🇲🇪 Montenegro"),  # обмежена мережа, але є Podgorica
        ("PT", "🇵🇹 Madeira/Azores"),  
    ]

    # Примітка: якщо для певної країни рейсів у мережі немає, кнопку можна тимчасово
    # прибрати. Основний перелік з офіційних сторінок Ryanair.

    builder = InlineKeyboardBuilder()
    for code, label in countries:
        builder.add(InlineKeyboardButton(text=label, callback_data=f"country:{code}"))

    builder.add(InlineKeyboardButton(text="🔙 Späť", callback_data="back"))
    # сітка 2–3 колонки виглядає охайно; можна підлаштувати під смак
    builder.adjust(2)
    return builder.as_markup()

def country_range_keyboard():
    """Період для пошуку по країні."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🗓 1 mesiac", callback_data="m:1"),
        InlineKeyboardButton(text="🗓 1–3 mesiace", callback_data="m:1-3"),
        InlineKeyboardButton(text="🗓 3–6 mesiacov", callback_data="m:3-6"),
        InlineKeyboardButton(text="🟢 Najlacnejšie (6 mes.)", callback_data="m:best6"),
        InlineKeyboardButton(text="🔙 Späť", callback_data="back"),
    )
    builder.adjust(1)
    return builder.as_markup()
