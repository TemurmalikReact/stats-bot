from aiogram import types
from sqlalchemy.future import select
from sqlalchemy import func
from database import AsyncSessionLocal
from models import Player, Stat


async def cmd_your_stats(message: types.Message):
    tg_id = message.from_user.id

    async with AsyncSessionLocal() as db:
        # Find player by Telegram ID
        player = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if not player:
            await message.answer("Вы ещё не зарегистрированы. Используйте /start.")
            return

        # Get player's goals (default 0 if no stat record yet)
        result = await db.execute(
            select(func.coalesce(Stat.goals, 0)).filter_by(player_id=player.id)
        )
        goals = result.scalar() or 0

    await message.answer(f"⚽ {player.name}, у вас {goals} гол(ов).")
