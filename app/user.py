from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.generators import gpt_text
from app.database.requests import set_user, get_user, calculate

from decimal import Decimal

user = Router()


class Chat(StatesGroup):
    text = State()
    wait = State()


class Image(StatesGroup):
    text = State()
    wait = State()


@user.message(F.text == 'Отмена')
@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id)
    await message.answer('Привет!!! Я бот с искусственным интеллектом. Напиши сообщение и я отвечу на него)',
                         reply_markup=kb.main)
    await state.clear()


@user.message(F.text == 'Генерация картинок')
async def chatting(message: Message, state: FSMContext):
    user_db = await get_user(message.from_user.id)
    if Decimal(user_db.balance) > 0:
        await state.set_state(Chat.text)
        await message.answer('Введите запрос', reply_markup=kb.cancel)
    else:
        await message.answer('Недостаточно средств на балансе')


@user.message()
async def chat_response(message: Message, state: FSMContext):
    user_db = await get_user(message.from_user.id)
    if Decimal(user_db.balance) > 0:
        await state.set_state(Chat.wait)
        response = await gpt_text(message.text, model='gpt-4o')
        await calculate(message.from_user.id, response['usage'], 'gpt-4o')
        await message.answer(response['response'])
        await state.set_state(Chat.text)
    else:
        await message.answer('Недостаточно средств на балансе')


@user.message(Chat.wait)
async def stop(massage: Message):
    await massage.answer('Не так быстро, дай мне придумать ответ!')

# ________________________________________________________________________

