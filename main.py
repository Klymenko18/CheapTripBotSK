import asyncio
from dotenv import load_dotenv
from aiogram.types import BotCommand
from app.bot.bot import bot, dp
from app.db.db import init_db
from app.handlers import register_handlers

load_dotenv()


async def set_bot_commands(bot):
    commands = [
        BotCommand(command="start", description="Start / Choose language"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Вимикаємо webhook, інакше Telegram блокує polling (Conflict)
    await bot.delete_webhook(drop_pending_updates=True)

    # 1) Ініціалізація БД
    init_db()

    # 2) Реєстрація хендлерів (у т.ч. /start → вибір мови)
    register_handlers(dp)

    # 3) Команди меню бота
    await set_bot_commands(bot)

    print("🚀 Bot started. Waiting for /start to choose language...")

    # 4) Запуск long polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
