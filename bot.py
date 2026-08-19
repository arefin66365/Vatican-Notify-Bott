import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)


async def send_message(text):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


async def check_vatican():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        await page.goto(
            "https://tickets.museivaticani.va/home",
            wait_until="networkidle"
        )

        title = await page.title()

        await send_message(
            f"🌐 Vatican page opened\nTitle: {title}"
        )

        await browser.close()


asyncio.run(check_vatican())
