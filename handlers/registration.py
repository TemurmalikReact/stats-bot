from aiogram import types, Dispatcher
from database import AsyncSessionLocal
from models import Player
import random

async def cmd_start(msg: types.Message):
    tg_id = msg.from_user.id
    async with AsyncSessionLocal() as db:
        exists = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if exists:
            await msg.answer(f"Вы уже зарегистрированы: ID {exists.ext_id}")
            return
        ext_id = random.randint(1, 999)
        # можно проверять на коллизию в цикле
        player = Player(tg_id=tg_id, ext_id=ext_id)
        db.add(player)
        await db.commit()
        await msg.answer(f"Добро пожаловать! Ваш ID: {ext_id}\nВведите ваше имя:")
        # сохраняем состояние FSM — ожидаем имя
