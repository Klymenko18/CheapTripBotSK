from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


BOT_TOKEN= "8034826002:AAHP8Fp9dOIDYi1LdtGbqFqALJuCjTMVpDc"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
