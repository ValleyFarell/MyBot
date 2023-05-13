from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterNewUser(StatesGroup):
    username_completion = State()
    type_completion = State()
    portfolio_completion = State()


class GuessNumberGame(StatesGroup):
    startgame_state = State()
    in_game_state = State()
    ending_game_state = State()
