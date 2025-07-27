import asyncio                    # ✅ Standard
import os                         # ✅ Needed for env vars
from aiogram import Bot, Dispatcher, types              # ✅ All valid from `aiogram`
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # ✅ FSM memory
from database import init_db     # ✅ You must have `database.py` with `init_db` defined
import registration              # ✅ You must have `registration.py` with `cmd_start`
import admin                     # ✅ You must have `admin.py` with `cmd_add_goals`
import stats                     # ✅ You must have `stats.py` with `cmd_top_goals`

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
