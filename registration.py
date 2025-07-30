import random
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy.future import select
from sqlalchemy import func
from database import AsyncSessionLocal
from models import Player

# FSM definition
class RegisterState(StatesGroup):
    waiting_for_name = State()

async def cmd_start(msg: types.Message, state: FSMContext):
    tg_id = msg.from_user.id
    async with AsyncSessionLocal() as db:
        # 1) If user already registered, early exit
        exists = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if exists:
            await msg.answer(f"Вы уже зарегистрированы: ID {exists.ext_id}")
            return

        # 2) Fetch all assigned ext_id values
        result = await db.execute(select(Player.ext_id))
        assigned = sorted(r[0] for r in result.all())

        # 3) Find the first missing positive integer
        new_id = 1
        for eid in assigned:
            if eid == new_id:
                new_id += 1
            elif eid > new_id:
                break
        # new_id is now the first available ext_id

    # 4) Store ext_id and tg_id in FSM (do not write to DB yet)
    await state.update_data(ext_id=new_id, tg_id=tg_id)
    await state.set_state(RegisterState.waiting_for_name)
    await msg.answer(f"Добро пожаловать! Введите ваше имя:")

async def process_name(msg: types.Message, state: FSMContext):
    name = msg.text.strip()
    data = await state.get_data()
    ext_id = data.get("ext_id")
    tg_id = data.get("tg_id")

    if not ext_id or not tg_id:
        await msg.answer("Ошибка: не удалось определить ваш ID. Повторите регистрацию.")
        await state.finish()
        return

    async with AsyncSessionLocal() as db:
        # Ensure no one else took this ext_id while user was typing name
        existing = await db.scalar(select(Player).filter_by(ext_id=ext_id))
        if existing:
            await msg.answer("Ошибка: этот ID уже занят. Повторите регистрацию.")
            await state.finish()
            return

        # Create and commit the new player with name now
        player = Player(tg_id=tg_id, ext_id=ext_id, name=name)
        db.add(player)
        await db.commit()
        await msg.answer(f"Имя сохранено как {name}, ваш ID: {ext_id} ✅")

    await state.finish()
