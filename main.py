import asyncio
from core.bot import bot
from core.dispatcher import dp

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
git