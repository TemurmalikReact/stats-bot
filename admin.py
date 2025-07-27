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

    parts = msg.text.split()
    if len(parts) < 3:
        await msg.answer("Неверный формат. Используйте: /add_goals <ext_id> <кол-во голов>")
        return

    try:
        ext_id, num = int(parts[1]), int(parts[2])
    except ValueError:
        await msg.answer("Ошибка: ext_id и количество голов должны быть числами.")
        return

    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(ext_id=ext_id))
        if not player:
            await msg.answer(f"Игрок с ext_id {ext_id} не найден.")
            return

        stat = await db.scalar(select(Stat).filter_by(player_id=player.id))
        if not stat:
            stat = Stat(player_id=player.id, goals=0)
            db.add(stat)

        stat.goals += num
        await db.commit()

        await msg.answer(f"Добавлено {num} голов игроку {ext_id}")
