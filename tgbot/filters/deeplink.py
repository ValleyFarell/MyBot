import re
import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config

pattern = re.compile(r"^[a-z0-9_-]{4, 15}$")


class DeeplinkFilter(BoundFilter):
    key = 'is_corr_deeplink'

    def __init__(self, is_corr_deeplink: typing.Optional[str] = None):
        self.is_corr_deeplink = is_corr_deeplink

    async def check(self, obj):
        if self.is_corr_deeplink is None:
            return False
        message_text = obj.text.split()[-1]
        return True if re.fullmatch(r"[0-9]{3,15}", string=message_text) != None else False
