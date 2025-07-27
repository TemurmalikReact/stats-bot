from aiogram import types
from sqlalchemy import select, desc
from database import AsyncSessionLocal
from models import Player, Stat

from sqlalchemy import desc, select
from models import Player, Stat
from database import AsyncSessionLocal

async def cmd_top_goals(message: types.Message):
    async with AsyncSessionLocal() as db:
        # Get top 5 players by goals
        result = await db.execute(
            select(Player.first_name, Player.last_name, Player.ext_id, Stat.goals)
            .join(Stat, Player.id == Stat.player_id)
            .order_by(desc(Stat.goals))
            .limit(5)
        )
        top_players = result.all()

        # Get all players with their ext_id and names
        all_players_result = await db.execute(
            select(Player.ext_id, Player.first_name, Player.last_name)
        )
        all_players = all_players_result.all()

    if not top_players:
        await message.answer("Статистика пока пуста.")
        return

    # Top-5 goal scorers
    text = "🏆 Топ‑5 бомбардиров:\n"
    for idx, (name, last_name, ext_id, goals) in enumerate(top_players, 1):
        text += f"{idx}. {name} {last_name} (ID {ext_id}) — {goals} гол(ов)\n"

    # All registered players
    text += "\n📋 Все игроки:\n"
    for ext_id, name, in all_players:
        text += f"ID {ext_id} — {name}\n"

    await message.answer(text)
