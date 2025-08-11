import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot_handlers import setup_handlers

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
setup_handlers(dp)  # register routes

async def main():
    print("Polling mode started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
