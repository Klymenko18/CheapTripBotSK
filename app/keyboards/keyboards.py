from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# ---------------- I18N ----------------

LANGS = ("en", "sk", "de", "uk")

TR = {
    "back": {
        "en": "🔙 Back",
        "sk": "🔙 Späť",
        "de": "🔙 Zurück",
        "uk": "🔙 Назад",
    },
    "months": {
        "en": {
            "08": "📅 8 August",
            "09": "📅 9 September",
            "10": "📅 10 October",
            "11": "📅 11 November",
            "12": "📅 12 December",
        },
        "sk": {
            "08": "📅 8 August",
            "09": "📅 9 September",
            "10": "📅 10 Október",
            "11": "📅 11 November",
            "12": "📅 12 December",
        },
        "de": {
            "08": "📅 8 August",
            "09": "📅 9 September",
            "10": "📅 10 Oktober",
            "11": "📅 11 November",
            "12": "📅 12 Dezember",
        },
        "uk": {
            "08": "📅 8 Серпень",
            "09": "📅 9 Вересень",
            "10": "📅 10 Жовтень",
            "11": "📅 11 Листопад",
            "12": "📅 12 Грудень",
        },
    },
    "price_buttons": {
        "en": ["💶 Up to €50", "💶 €50–80", "💶 €80–100", "🟢 Cheapest", "🌟 All"],
        "sk": ["💶 Do 50€", "💶 50–80€", "💶 80–100€", "🟢 Najlacnejšie", "🌟 Všetky"],
        "de": ["💶 Bis 50€", "💶 50–80€", "💶 80–100€", "🟢 Am günstigsten", "🌟 Alle"],
        "uk": ["💶 До 50€", "💶 50–80€", "💶 80–100€", "🟢 Найдешевші", "🌟 Усі"],
    },
    "return_buttons": {
        "en": ["↩️ In 1–3 days", "↩️ In 3–5 days", "↩️ In 5–10 days", "🟢 Cheapest (≤2 weeks)"],
        "sk": ["↩️ O 1–3 dni", "↩️ O 3–5 dní", "↩️ O 5–10 dní", "🟢 Najlacnejšie (do 2 týždňov)"],
        "de": ["↩️ In 1–3 Tagen", "↩️ In 3–5 Tagen", "↩️ In 5–10 Tagen", "🟢 Am günstigsten (≤2 Wochen)"],
        "uk": ["↩️ Через 1–3 дні", "↩️ Через 3–5 днів", "↩️ Через 5–10 днів", "🟢 Найдешевше (до 2 тижнів)"],
    },
    "country_mode": {
        "en": ("🌍 All countries", "🎯 Specific country"),
        "sk": ("🌍 Všetky krajiny", "🎯 Konkrétna krajina"),
        "de": ("🌍 Alle Länder", "🎯 Spezifisches Land"),
        "uk": ("🌍 Усі країни", "🎯 Конкретна країна"),
    },
    "country_period": {
        "en": ["🗓 1 month", "🗓 1–3 months", "🗓 3–6 months", "🟢 Cheapest (6 mo.)"],
        "sk": ["🗓 1 mesiac", "🗓 1–3 mesiace", "🗓 3–6 mesiacov", "🟢 Najlacnejšie (6 mes.)"],
        "de": ["🗓 1 Monat", "🗓 1–3 Monate", "🗓 3–6 Monate", "🟢 Am günstigsten (6 Mon.)"],
        "uk": ["🗓 1 місяць", "🗓 1–3 місяці", "🗓 3–6 місяців", "🟢 Найдешевше (6 міс.)"],
    },
    "origin_labels": {
        "en": [("🇸🇰 Bratislava", "BTS"), ("🇸🇰 Košice", "KSC"), ("🇦🇹 Vienna", "VIE")],
        "sk": [("🇸🇰 Bratislava", "BTS"), ("🇸🇰 Košice", "KSC"), ("🇦🇹 Viedeň", "VIE")],
        "de": [("🇸🇰 Bratislava", "BTS"), ("🇸🇰 Košice", "KSC"), ("🇦🇹 Wien", "VIE")],
        "uk": [("🇸🇰 Братислава", "BTS"), ("🇸🇰 Кошице", "KSC"), ("🇦🇹 Відень", "VIE")],
    },
}

def _lang(lang: str) -> str:
    return lang if lang in LANGS else "en"

# ---------------- Language keyboard ----------------
def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="English", callback_data="lang:en"),
        InlineKeyboardButton(text="Slovakian", callback_data="lang:sk"),
        InlineKeyboardButton(text="German", callback_data="lang:de"),
        InlineKeyboardButton(text="Українська", callback_data="lang:uk"),
    )
    builder.adjust(2)
    return builder.as_markup()

# ---------------- Keyboards (with i18n) ----------------
def month_keyboard(lang: str = "en"):
    lang = _lang(lang)
    builder = InlineKeyboardBuilder()
    for code, label in TR["months"][lang].items():
        builder.add(InlineKeyboardButton(text=label, callback_data=code))
    builder.add(InlineKeyboardButton(text=TR["back"][lang], callback_data="back"))
    builder.adjust(3)
    return builder.as_markup()

def price_keyboard(lang: str = "en"):
    lang = _lang(lang)
    texts = TR["price_buttons"][lang]
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=texts[0], callback_data="p:<=50"),
        InlineKeyboardButton(text=texts[1], callback_data="p:50-80"),
        InlineKeyboardButton(text=texts[2], callback_data="p:80-100"),
        InlineKeyboardButton(text=texts[3], callback_data="p:cheapest"),
        InlineKeyboardButton(text=texts[4], callback_data="p:all"),
        InlineKeyboardButton(text=TR["back"][lang], callback_data="back"),
    )
    builder.adjust(2)
    return builder.as_markup()

def origin_keyboard(lang: str = "en"):
    lang = _lang(lang)
    builder = InlineKeyboardBuilder()
    for name, code in TR["origin_labels"][lang]:
        builder.add(InlineKeyboardButton(text=name, callback_data=f"origin:{code}"))
    builder.add(InlineKeyboardButton(text=TR["back"][lang], callback_data="back"))
    builder.adjust(2)
    return builder.as_markup()

def return_range_keyboard(lang: str = "en"):
    lang = _lang(lang)
    texts = TR["return_buttons"][lang]
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=texts[0], callback_data="r:1-3"),
        InlineKeyboardButton(text=texts[1], callback_data="r:3-5"),
        InlineKeyboardButton(text=texts[2], callback_data="r:5-10"),
        InlineKeyboardButton(text=texts[3], callback_data="r:cheap14"),
        InlineKeyboardButton(text=TR["back"][lang], callback_data="back"),
    )
    builder.adjust(1)
    return builder.as_markup()

# --- режим "країна" ---
def country_mode_keyboard(lang: str = "en"):
    lang = _lang(lang)
    all_lbl, pick_lbl = TR["country_mode"][lang]
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=all_lbl, callback_data="country_mode:all"),
        InlineKeyboardButton(text=pick_lbl, callback_data="country_mode:pick"),
        InlineKeyboardButton(text=TR["back"][lang], callback_data="back"),
    )
    builder.adjust(1)
    return builder.as_markup()

def country_select_keyboard(lang: str = "en"):
    """Вибір країни (із локалізованою кнопкою Back)."""
    lang = _lang(lang)
    countries = [
        ("IT", "🇮🇹 Italy"), ("ES", "🇪🇸 Spain"), ("FR", "🇫🇷 France"),
        ("PT", "🇵🇹 Portugal"), ("NL", "🇳🇱 Netherlands"), ("DE", "🇩🇪 Germany"),
        ("PL", "🇵🇱 Poland"), ("AT", "🇦🇹 Austria"), ("BE", "🇧🇪 Belgium"),
        ("IE", "🇮🇪 Ireland"), ("GB", "🇬🇧 United Kingdom"), ("CH", "🇨🇭 Switzerland"),
        ("SE", "🇸🇪 Sweden"), ("NO", "🇳🇴 Norway"), ("DK", "🇩🇰 Denmark"),
        ("FI", "🇫🇮 Finland"), ("EE", "🇪🇪 Estonia"), ("LV", "🇱🇻 Latvia"),
        ("LT", "🇱🇹 Lithuania"), ("LU", "🇱🇺 Luxembourg"), ("MT", "🇲🇹 Malta"),
        ("GR", "🇬🇷 Greece"), ("CY", "🇨🇾 Cyprus"), ("HR", "🇭🇷 Croatia"),
        ("SI", "🇸🇮 Slovenia"), ("CZ", "🇨🇿 Czech Republic"),
        ("HU", "🇭🇺 Hungary"), ("RO", "🇷🇴 Romania"), ("BG", "🇧🇬 Bulgaria"),
        ("AL", "🇦🇱 Albania"), ("BA", "🇧🇦 Bosnia and Herzegovina"),
        ("ME", "🇲🇪 Montenegro"),
    ]
    builder = InlineKeyboardBuilder()
    for code, label in countries:
        builder.add(InlineKeyboardButton(text=label, callback_data=f"country:{code}"))
    builder.add(InlineKeyboardButton(text=TR["back"][lang], callback_data="back"))
    builder.adjust(2)
    return builder.as_markup()

def country_range_keyboard(lang: str = "en"):
    lang = _lang(lang)
    texts = TR["country_period"][lang]
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=texts[0], callback_data="m:1"),
        InlineKeyboardButton(text=texts[1], callback_data="m:1-3"),
        InlineKeyboardButton(text=texts[2], callback_data="m:3-6"),
        InlineKeyboardButton(text=texts[3], callback_data="m:best6"),
        InlineKeyboardButton(text=TR["back"][lang], callback_data="back"),
    )
    builder.adjust(1)
    return builder.as_markup()
