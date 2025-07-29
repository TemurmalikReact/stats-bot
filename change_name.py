from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy.future import select
from database import AsyncSessionLocal
from models import Player


class ChangeNameState(StatesGroup):
    waiting_for_new_name = State()


# /change_name command — initiates name change
async def cmd_change_name(msg: types.Message, state: FSMContext):
    tg_id = msg.from_user.id
    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if not player:
            await msg.answer("Вы ещё не зарегистрированы. Используйте /start.")
            return

    await state.set_state(ChangeNameState.waiting_for_new_name)
    await msg.answer("Введите ваше новое имя:")


# Handle new name input and save it
async def process_new_name(msg: types.Message, state: FSMContext):
    new_name = msg.text.strip()
    tg_id = msg.from_user.id

    async with AsyncSessionLocal() as db:
        player = await db.scalar(select(Player).filter_by(tg_id=tg_id))
        if player:
            player.name = new_name
            db.add(player)
            await db.commit()
            await msg.answer(f"Имя успешно изменено на {new_name} ✅")
        else:
            await msg.answer("Ошибка: игрок не найден.")

    await state.finish()
