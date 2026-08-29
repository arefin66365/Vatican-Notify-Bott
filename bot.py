import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

URL = "https://tickets.museivaticani.va/home/visit/1/1788732000000/1"


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

        try:
            await page.goto(
                URL,
                wait_until="networkidle",
                timeout=60000
            )

            await page.wait_for_timeout(8000)

            text = await page.locator("body").inner_text()

            if "10:00" in text or "10.00" in text:

                await send_message(
                    "🎉 Vatican Slot Available!\n\n"
                    "📅 Date: 7 September 2026\n"
                    "⏰ Time: 10:00 AM\n"
                    "🎟 Vatican Museums + Sistine Chapel\n\n"
                    f"🔗 {URL}"
                )

            else:

                await send_message(
                    "🔎 Page checked.\n\n"
                    "Current page text:\n\n"
                    + text[:2000]
                )

        except Exception as e:

            await send_message(
                f"⚠️ Error:\n{e}"
            )

        finally:

            await browser.close()


asyncio.run(check_vatican())