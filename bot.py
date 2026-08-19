import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)


async def send_message(message):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


async def check_vatican():

    url = "https://tickets.museivaticani.va/"

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        await page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        content = await page.content()

        if "Vatican" in content:
            await send_message(
                "✅ Vatican Museums page checked successfully"
            )
        else:
            await send_message(
                "❌ Vatican page not loaded"
            )

        await browser.close()


asyncio.run(check_vatican())
