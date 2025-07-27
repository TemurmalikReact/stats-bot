import os
from aiogram import types
from database import AsyncSessionLocal      # ✅ You must have this defined in `database.py`
from models import Player, Stat             # ✅ Must exist in `models.py`
from sqlalchemy.future import select        # ❗️MISSING IMPORT HERE


async def cmd_add_goals(msg: types.Message):
    admin_id = os.getenv("ADMIN_ID")
    if admin_id is None:
        await msg.answer("Ошибка: ADMIN_ID не настроен.")
        return
    if msg.from_user.id != int(admin_id):
        await msg.answer("У вас нет прав для этой команды.")
        return
    if msg.from_user.id != int(os.getenv("ADMIN_ID")):
        return
    parts = msg.text.split()
    ext_id, num = int(parts[1]), int(parts[2])
    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(ext_id=ext_id))
        stat = await db.scalar(select(Stat).filter_by(player_id=player.id))
        if not stat:
            stat = Stat(player_id=player.id)
            db.add(stat)
        stat.goals += num
        await db.commit()
        await msg.answer(f"Добавлено {num} голов игроку {ext_id}")
