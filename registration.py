import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Player
from sqlalchemy import func

# FSM definition
class RegisterState(StatesGroup):
    waiting_for_name = State()


# /start command — registration starts here
async def cmd_start(msg: types.Message, state: FSMContext):
    tg_id = msg.from_user.id
    async with AsyncSessionLocal() as db:
        exists = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if exists:
            await msg.answer(f"Вы уже зарегистрированы: ID {exists.ext_id}")
            return


        ext_id=tg_id
        player = Player(tg_id=tg_id, ext_id=ext_id)

        db.add(player)
        await db.commit()

    await state.update_data(ext_id=ext_id)
    await state.set_state(RegisterState.waiting_for_name)
    await msg.answer(f"Добро пожаловать! Ваш ID: {ext_id}\nВведите ваше имя:")


# Handle name input and save it using ext_id
async def process_name(msg: types.Message, state: FSMContext):
    name = msg.text.strip()
    data = await state.get_data()
    ext_id = data.get("ext_id")

    if not ext_id:
        await msg.answer("Ошибка: не удалось определить ваш ID. Повторите регистрацию.")
        await state.finish()
        return

    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(ext_id=ext_id))
        if player:
            player.name = name
            db.add(player)
            await db.commit()
            await msg.answer(f"Имя сохранено как {name} ✅")
        else:
            await msg.answer("Ошибка: игрок не найден.")
    
    await state.finish()
