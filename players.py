
import os
from aiogram import types
from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from database import AsyncSessionLocal
from models import Player, Stat

async def cmd_all_players(message: types.Message):
    async with AsyncSessionLocal() as db:
        # Outer join to include players without stats
        result = await db.execute(
            select(Player.name, Player.ext_id, func.coalesce(Stat.goals, 0))
            .outerjoin(Stat, Player.id == Stat.player_id)
            .order_by(Player.ext_id)
        )
        all_players = result.all()

    if not all_players:
        await message.answer("Игроки пока не зарегистрированы.")
        return

    admin_id = os.getenv("ADMIN_ID")
    is_admin = message.from_user.id == int(admin_id) if admin_id else False

    text = "📋 Все игроки и их голы:\n"
    for idx, (name, ext_id, goals) in enumerate(all_players, 1):
        if is_admin:
            text += f"{idx}. {name} (ID {ext_id}) — {goals} гол(ов)\n"
        else:
            text += f"{idx}. {name} — {goals} гол(ов)\n"

    await message.answer(text)
