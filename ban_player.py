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
        await msg.answer("Используйте: /ban_player <ext_id>")
        return

    try:
        ext_id = int(args[1])
    except ValueError:
        await msg.answer("❌ Некорректный формат ID. Используйте числовой ext_id.")
        return

    async with AsyncSessionLocal() as db:
        # Find by ext_id
        player = await db.scalar(select(Player).filter_by(ext_id=ext_id))

        if not player:
            await msg.answer("Игрок с таким ID не найден.")
            return

        # Ban their Telegram ID (if exists)
        if not player.tg_id:
            await msg.answer("❌ У этого игрока нет Telegram ID — невозможно заблокировать.")
            return

        player.banned = True
        await db.commit()
        await msg.answer(f"✅ Игрок {player.name} (ext_id: {player.ext_id}, tg_id: {player.tg_id}) заблокирован навсегда.")
