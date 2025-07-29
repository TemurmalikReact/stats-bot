import os
from aiogram import types
from database import AsyncSessionLocal
from models import Player, Stat
from sqlalchemy.future import select
from sqlalchemy import delete


async def cmd_delete_player(msg: types.Message):
    admin_id = os.getenv("ADMIN_ID")
    if admin_id is None:
        await msg.answer("Ошибка: ADMIN_ID не настроен.")
        return
    if msg.from_user.id != int(admin_id):
        await msg.answer("У вас нет прав для этой команды.")
        return

    parts = msg.text.split()
    if len(parts) != 2:
        await msg.answer("Неверный формат. Используйте: /delete_player <ext_id>")
        return

    try:
        ext_id = int(parts[1])
    except ValueError:
        await msg.answer("Ошибка: ext_id должен быть числом.")
        return

    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(ext_id=ext_id))
        if not player:
            await msg.answer(f"Игрок с ext_id {ext_id} не найден.")
            return

        # Delete the stat first (if exists), then the player
        await db.execute(delete(Stat).where(Stat.player_id == player.id))
        await db.delete(player)
        await db.commit()

        await msg.answer(f"Игрок с ext_id {ext_id} и его статистика удалены.")
