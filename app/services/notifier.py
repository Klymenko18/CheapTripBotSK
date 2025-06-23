from app.bot.bot import bot

def notify_users(user_id: int, text: str):
    try:
        from asyncio import create_task
        create_task(bot.send_message(chat_id=user_id, text=text))
    except Exception as e:
        print(f"❗ Error sending message to {user_id}: {e}")
