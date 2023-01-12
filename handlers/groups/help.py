from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from filters import IsGroup


@dp.message_handler(IsGroup(), CommandHelp())
async def bot_help(message: types.Message):
    text = ("Commands: ",
            "/start - Adds you into DB",
            "/help - Simple help command",)

    await message.answer("\n".join(text))
