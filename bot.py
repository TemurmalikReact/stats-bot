import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from database import init_db
import registration
import admin
import stats
import players
import change_name
import delete_player

async def on_startup(dp):
    await init_db()

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set")

    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Register handlers
    dp.register_message_handler(registration.cmd_start, commands=["start"], state="*")
    dp.register_message_handler(registration.process_name, state=registration.RegisterState.waiting_for_name)

    dp.register_message_handler(admin.cmd_add_goals, commands=["add_goals"])
    dp.register_message_handler(stats.cmd_top_goals, commands=["top_goals"])
    dp.register_message_handler(players.cmd_all_players, commands=["all_players"])
    dp.register_message_handler(delete_player.cmd_delete_player, commands=["delete_player"])

    dp.register_message_handler(change_name.cmd_change_name, commands=["change_name"], state="*")  # <-- New
    dp.register_message_handler(change_name.process_new_name, state=change_name.ChangeNameState.waiting_for_new_name)  # <-- New

    executor.start_polling(dp, on_startup=on_startup)

if __name__ == "__main__":
    main()
