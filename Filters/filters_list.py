from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import dp, admins


class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        # member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        # print(message.from_user.id in admins)
        return message.from_user.id in admins


dp.filters_factory.bind(MyFilter)
