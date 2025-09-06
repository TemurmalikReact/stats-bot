import os
from aiogram import types
from sqlalchemy import update
from database import AsyncSessionLocal
from models import Stat

async def cmd_reset_stats(msg: types.Message):
    admin_id = os.getenv("ADMIN_ID")
    if admin_id is None:
        await msg.answer("Ошибка: ADMIN_ID не настроен.")
        return
    if msg.from_user.id != int(admin_id):
        await msg.answer("У вас нет прав для этой команды.")
        return

    async with AsyncSessionLocal() as db:
        # ✅ Use async execute with update
        await db.execute(update(Stat).values(goals=0))
        await db.commit()

    await msg.answer("✅ Все голы обнулены!")
