import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Player


# FSM definition (v2 style)
class RegisterState(StatesGroup):
    waiting_for_name = State()


# /start command
async def cmd_start(msg: types.Message, state: FSMContext):
    tg_id = msg.from_user.id
    async with AsyncSessionLocal() as db:
        exists = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if exists:
            await msg.answer(f"Вы уже зарегистрированы: ID {exists.ext_id}")
            return
        ext_id = random.randint(1, 999)
        player = Player(tg_id=tg_id, ext_id=ext_id)
        db.add(player)
        await db.commit()

    await msg.answer(f"Добро пожаловать! Ваш ID: {ext_id}\nВведите ваше имя:")
    await state.set_state(RegisterState.waiting_for_name)


# name handler
async def process_name(msg: types.Message, state: FSMContext):
    name = msg.text.strip()
    tg_id = msg.from_user.id
    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if player:
            player.name = name
            db.add(player)
            await db.commit()
    await state.finish()
    await msg.answer(f"Имя сохранено как {name} ✅")
