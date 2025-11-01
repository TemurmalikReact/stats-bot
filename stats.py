import os
from aiogram import types
from sqlalchemy import select, desc, func
from sqlalchemy.orm import aliased
from database import AsyncSessionLocal
from models import Player, Stat

async def cmd_top_goals(message: types.Message):
    async with AsyncSessionLocal() as db:
        # LEFT JOIN to include players without stats
        result = await db.execute(
            select(
                Player.name,
                Player.ext_id,
                func.coalesce(Stat.goals, 0).label("goals")
            )
            .outerjoin(Stat, Player.id == Stat.player_id)  # LEFT JOIN
            .order_by(desc("goals"))
            .limit(70)
        )
        top_players = result.all()

    text = "🏆 Топ-70 бомбардиров:\n"
    for idx, (name, ext_id, goals) in enumerate(top_players, 1):
        text += f"{idx}. {name} (ID {ext_id}) — {goals} гол(ов)\n"

    await message.answer(text)
