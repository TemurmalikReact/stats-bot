import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import init_db
import registration
import admin
import stats

async def main():
    await init_db()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    dp.register_message_handler(registration.cmd_start, commands=["start"])
    # … FSM‑хэндлеры на ввод имени/фамилии
    dp.register_message_handler(admin.cmd_add_goals, commands=["add_goals"])
    # … остальные админ‑команды
    dp.register_message_handler(stats.cmd_top_goals, commands=["top_goals"])
    # …

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
