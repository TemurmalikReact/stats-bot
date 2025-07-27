from aiogram import types
from sqlalchemy import select, func, desc
from database import AsyncSessionLocal
from models import Player, Stat

async def cmd_top_goals(message: types.Message):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Player.first_name, Player.last_name, Player.ext_id, Stat.goals)
            .join(Stat, Player.id == Stat.player_id)
            .order_by(desc(Stat.goals))
            .limit(10)
        )
        top_players = result.all()

    if not top_players:
        await message.answer("Статистика пока пуста.")
        return

    text = "🏆 Топ‑10 бомбардиров:\n"
    for idx, (first_name, last_name, ext_id, goals) in enumerate(top_players, 1):
        full_name = f"{first_name or ''} {last_name or ''}".strip()
        text += f"{idx}. {full_name} (ID {ext_id}) — {goals} гол(ов)\n"

    await message.answer(text)


async def cmd_all_players(message: types.Message):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Player.first_name, Player.last_name, Player.ext_id, func.coalesce(Stat.goals, 0))
            .outerjoin(Stat, Player.id == Stat.player_id)
            .order_by(Player.ext_id)
        )
        players = result.all()

    if not players:
        await message.answer("Игроки пока не зарегистрированы.")
        return

    text = "📋 Все игроки и их голы:\n"
    for idx, (first_name, last_name, ext_id, goals) in enumerate(players, 1):
        full_name = f"{first_name or ''} {last_name or ''}".strip()
        text += f"{idx}. {full_name} (ID {ext_id}) — {goals} гол(ов)\n"

    await message.answer(text)
