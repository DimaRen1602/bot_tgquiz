import asyncio
from config import dp, bot
from handlers import start_handler, quiz_handler, callbacks
from utils.db_utils import create_table

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
