import os
from aiogram import types
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Player

async def cmd_ban_player(msg: types.Message):
    admin_id = os.getenv("ADMIN_ID")
    if admin_id is None or msg.from_user.id != int(admin_id):
        await msg.answer("У вас нет прав для этой команды.")
        return

    args = msg.text.split()
    if len(args) < 2:
        await msg.answer("Используйте: /ban_player <ext_id или tg_id>")
        return

    identifier = args[1]
    async with AsyncSessionLocal() as db:
        # Try to find by ext_id first, fallback to tg_id
        player = await db.scalar(select(Player).filter(
            (Player.ext_id == identifier) | (Player.tg_id == identifier)
        ))

        if not player:
            await msg.answer("Игрок не найден.")
            return

        player.banned = True
        await db.commit()
        await msg.answer(f"Игрок {player.name} (ID: {player.ext_id}) забанен.")
