import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)


async def send_message():
    await bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Vatican Bot is working!"
    )


asyncio.run(send_message())
