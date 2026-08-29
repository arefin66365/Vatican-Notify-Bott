import os
import asyncio
from telegram import Bot
from playwright.async_api import async_playwright

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

URL = "https://tickets.museivaticani.va/home/visit/1/1788732000000/1"

TARGET_DATE = "7 September 2026"
TARGET_TIME = "10:00"


async def send_message(message):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
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

            page_text = await page.locator(
                "body"
            ).inner_text()


            # Check date
            if TARGET_DATE.lower() not in page_text.lower():

                print("Date not found")
                await browser.close()
                return


            # Check time
            if TARGET_TIME in page_text:

                await send_message(
                    "🎉 VATICAN TICKET AVAILABLE!\n\n"
                    "📅 Date: 7 September 2026\n"
                    "⏰ Time: 10:00 AM\n"
                    "🎟 Vatican Museums + Sistine Chapel\n\n"
                    "Book now:\n"
                    f"{URL}"
                )

                print("AVAILABLE")


            else:

                print("10:00 slot not available")


        except Exception as e:

            print("Error:", e)


        finally:

            await browser.close()



asyncio.run(check_vatican())