import math
import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.storage import FSMContextProxy
from random import randint
from tgbot.misc.states import GuessNumberGame


corr_answer: int
max_count: int
async def start_game(message: types.Message):
    await message.answer(f"Доброго времени суток, мой дорогой друг!\n"
                        f"Для выхода введите команду /quit_game\n"
                        f"Для начала игры задайте диапазон возможных чисел, отправив сообщение по шаблону число/число")
    await message.answer(f"Примеры: 100/10000   -9/1    5/80")
    await GuessNumberGame.startgame_state.set()


async def set_range_of_numbers(message: types.Message, state=FSMContext):
    mess_text = message.text
    if re.fullmatch(r"-?[0-9]{1,50}/-?[0-9]{1,50}", string=mess_text) != None:
        left_range, right_range = map(int, mess_text.split('/'))
        if left_range >= right_range:
            await message.answer(f"""Вы неправильно ввели числа! Первое число всегда должно быть меньше второго.""")
        else:
            global corr_answer, max_count
            max_count = (right_range - left_range) // 2
            await message.answer(f"Число из диапазона [{left_range}; {right_range}] задано, кол-во попыток - {max_count}, дерзайте)")
            corr_answer = randint(left_range, right_range)
            print(corr_answer)
            await state.finish()
            await GuessNumberGame.in_game_state.set()
    else:
        await message.answer(f"Вы неправильно ввели числа! Нужно ввести числа по шаблону число-число и только неотрицательные. \n")


async def game(message: types.Message, state=FSMContext):
    global corr_answer, max_count
    answer = message.text
    if re.fullmatch(r"[0-9]{1,50}", string=answer) != None:
        if max_count == 0:
            await message.answer('Вы исчерпали все попытки и проиграли (')
            await message.answer('Если хотите начать заново, введите /game')
            await state.finish()
        max_count -= 1
        if int(answer) < corr_answer:
            print(int(answer))
            await message.answer('Больше')
        elif int(answer) > corr_answer:
            await message.answer('Меньше')
        else:
            await message.answer('Поздравляю, вы угадали!')
            await message.answer('Если хотите начать заново, введите /game')
            await state.finish()
    else:
        await message.answer('Введите число!')

async def quit_game(message: types.Message, state=FSMContext):
    await message.answer('Вы вышли из игры. До свидания!')
    await state.finish()


def register_game(dp: Dispatcher):
    dp.register_message_handler(start_game, commands=["game"])
    dp.register_message_handler(quit_game, state=GuessNumberGame.startgame_state, commands=['quit_game'])
    dp.register_message_handler(quit_game, state=GuessNumberGame.in_game_state, commands=['quit_game'])
    dp.register_message_handler(game, state=GuessNumberGame.in_game_state)
    dp.register_message_handler(set_range_of_numbers, state=GuessNumberGame.startgame_state)
