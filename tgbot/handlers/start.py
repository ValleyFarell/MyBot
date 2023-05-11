import re

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import get_start_link


async def bot_start_deeplink_private(message: types.Message):
    ref = message.get_args()
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f'Вы находитесь в приватной переписке \n'
                         f'В вашей команде есть диплинк \n'
                         f'Вы передали аргумент {ref}\n')


async def bot_start_private(message: types.Message):
    deeplink = await get_start_link(payload='123')
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f'Вы находитесь в приватной переписке \n'
                         f'В вашей команде нет диплинка \n'
                         f'Ваша диплинк ссылка - {deeplink}\n')


async def bot_start_group(message: types.Message):
    deeplink = await get_start_link(payload='123')
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f'Вы находитесь в группе {message.chat.full_name}\n'
                         f'Ваша диплинк ссылка - {deeplink}\n')


def register_start(dp: Dispatcher):
    dp.register_message_handler(
        bot_start_deeplink_private,
        commands='start',
        is_corr_deeplink=True,
        is_private_chat=True
    )
    dp.register_message_handler(bot_start_private, commands='start', is_private_chat=True)
    dp.register_message_handler(bot_start_group, commands='start')
