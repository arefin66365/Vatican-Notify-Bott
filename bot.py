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

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(
            "https://tickets.museivaticani.va/",
            wait_until="networkidle",
            timeout=60000
        )

        buttons = await page.get_by_text("BOOK").count()

await send_message(f"BOOK button count: {buttons}")

        if buttons > 0:
            await send_message(
                "🎉 Vatican Ticket Available!\n\n"
                "✅ Vatican Museums ticket found.\n"
                "🔗 https://tickets.museivaticani.va/"
            )

        # No ticket হলে কোনো message যাবে না

        await browser.close()


asyncio.run(check_vatican())