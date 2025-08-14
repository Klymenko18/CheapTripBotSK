from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import os

# Завантажуємо токен з .env
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set (put it into .env)")

# Створюємо екземпляр бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher зберігатиме стан для вибору мови при /start
dp = Dispatcher()

# Функція старту бота
async def on_startup():
    print("🚀 Bot is running. Waiting for /start to choose language...")
