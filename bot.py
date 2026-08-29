import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

DATE = "07/09/2026"


async def send_message(text):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


async def check_vatican():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(
                "https://tickets.museivaticani.va/",
                wait_until="networkidle",
                timeout=60000
            )

            # Search date/product availability
            await page.wait_for_timeout(5000)

            content = await page.content()

            if "07/09/2026" in content or "7 September 2026" in content:

                # Find available time text
                text = await page.locator("body").inner_text()

                await send_message(
                    "🎉 Vatican Ticket Available!\n\n"
                    "📅 Date: 7 September 2026\n"
                    "🎟 Vatican Museums + Sistine Chapel\n\n"
                    "Check website:\n"
                    "https://tickets.museivaticani.va/"
                )

            else:
    await send_message("🔎 Vatican check completed. No slot found for 7 September 2026")

        except Exception as e:
            print(e)

        finally:
            await browser.close()


asyncio.run(check_vatican())