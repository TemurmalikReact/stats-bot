import os
from aiogram import types
from sqlalchemy import select, desc
from database import AsyncSessionLocal
from models import Player, Stat

async def cmd_top_goals(message: types.Message):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Player.name, Player.ext_id, Stat.goals)
            .join(Stat, Player.id == Stat.player_id)
            .order_by(desc(Stat.goals))
            .limit(5)
        )
        top_players = result.all()

    if not top_players:
        await message.answer("Статистика пока пуста.")
        return

    admin_id = os.getenv("ADMIN_ID")
    is_admin = message.from_user.id == int(admin_id) if admin_id else False

    text = "🏆 Топ‑5 бомбардиров:\n"
    for idx, (name, ext_id, goals) in enumerate(top_players, 1):
        if is_admin:
            text += f"{idx}. {name} (ID {ext_id}) — {goals} гол(ов)\n"
        else:
            text += f"{idx}. {name} — {goals} гол(ов)\n"

    await message.answer(text)
