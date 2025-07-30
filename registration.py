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
        # now new_id is either a gap or max+1

        # 4) Create the new player with that ext_id
        player = Player(tg_id=tg_id, ext_id=new_id)
        db.add(player)
        await db.commit()

    # 5) Store ext_id in FSM and prompt for name
    await state.update_data(ext_id=new_id)
    await state.set_state(RegisterState.waiting_for_name)
    await msg.answer(f"Добро пожаловать! Ваш ID: {new_id}\nВведите ваше имя:")

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
