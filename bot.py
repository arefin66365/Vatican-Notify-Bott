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

            # Debug: page কী দেখছে তার কিছু অংশ পাঠাবে
            preview = text[:1000]

            if "07/09/2026" in text or "7 September 2026" in text:

                await send_message(
                    "🎉 Vatican Slot Found!\n\n"
                    "📅 Date: 7 September 2026\n"
                    "🎟 Vatican Museums + Sistine Chapel\n\n"
                    f"🔗 {URL}"
                )

            else:

                await send_message(
                    "🔎 Vatican check completed.\n"
                    "❌ 7 September 2026 not found.\n\n"
                    "Page preview:\n"
                    f"{preview}"
                )

        except Exception as e:

            await send_message(
                f"⚠️ Vatican Bot Error:\n{e}"
            )

        finally:

            await browser.close()


asyncio.run(check_vatican())