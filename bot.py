import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from database import init_db
import registration
import admin
import stats

async def on_startup(dp):
    await init_db()

def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Register handlers
    dp.register_message_handler(registration.cmd_start, commands=["start"], state="*")
    dp.register_message_handler(registration.process_name, state=registration.RegisterState.waiting_for_name)

    dp.register_message_handler(admin.cmd_add_goals, commands=["add_goals"])
    dp.register_message_handler(stats.cmd_top_goals, commands=["top_goals"])
    dp.register_message_handler(stats.cmd_all_players, commands=["all_players"])

    executor.start_polling(dp, on_startup=on_startup)

if __name__ == "__main__":
    main()
