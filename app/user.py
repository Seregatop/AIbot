from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.generators import gpt_text

user = Router()


class Work(StatesGroup):
    process = State()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!!! Я бот с искусственным интеллектом. Напиши сообщение и я отвечу на него)')


@user.message(Work.process)
async def stop(massage: Message):
    await massage.answer('Не так быстро, дай мне придумать ответ!')


@user.message()
async def ai(massage: Message, state: FSMContext):
    await state.set_state(Work.process)
    res = await gpt_text(massage.text, model='gpt-4o-mini')
    await massage.answer(res)
    await state.clear()
