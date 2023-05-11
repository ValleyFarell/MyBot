import typing
from aiogram import types

from aiogram.dispatcher.filters import BoundFilter


class IsPrivateChat(BoundFilter):
    key = "is_private_chat"

    def __init__(self, is_private_chat: typing.Optional[bool] = None):
        self.is_private_chat = is_private_chat

    async def check(self, message: types.Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
