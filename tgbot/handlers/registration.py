from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.storage import FSMContextProxy

from tgbot.misc.states import RegisterNewUser


async def registration_begin(message: types.Message):
    await message.answer("Приветсвую! Вы запустили регистрацию. Пожалуйста, введите имя")
    await RegisterNewUser.username_completion.set()


async def username_complit(message: types.Message, state=FSMContext):
    username = message.text
    # await state.update_data(username1=username)
    # await state.update_data({"username1": username})
    async with state.proxy() as data:
        data['username1'] = username
    await message.answer(f"Отлично, {username}! \n"
                         f"Вы: \n"
                         f"1) Учитель \n"
                         f"2) Ученик ")
    await RegisterNewUser.type_completion.set()


async def type_complit(message: types.Message, state=FSMContext):
    type_ = message.text
    # await state.update_data(type_1=type_)
    async with state.proxy() as data:
        data['type_1'] = type_
    data = await state.get_data()
    await message.reply(f'Супер! Вы зарегестрированы: \n'
                        f'Ваше имя - {data.get("username1")}\n'
                        f'Вы {data.get("type_1")}\n')
    await RegisterNewUser.portfolio_completion.set()
    await state.finish()


def register_registrations(dp: Dispatcher):
    dp.register_message_handler(registration_begin, text='/reg')
    dp.register_message_handler(username_complit, state=RegisterNewUser.username_completion)
    dp.register_message_handler(type_complit, state=RegisterNewUser.type_completion)
