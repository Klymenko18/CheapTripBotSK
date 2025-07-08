import asyncio
import os
from dotenv import load_dotenv
from aiogram.types import BotCommand
from app.bot.bot import bot, dp
from app.db.db import init_db
from app.handlers import register_handlers

load_dotenv()

async def set_bot_commands(bot):
    commands = [
        BotCommand(command="start", description="Start"),
    ]
    await bot.set_my_commands(commands)

async def main():
    init_db()
    register_handlers(dp)
    await set_bot_commands(bot)
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
