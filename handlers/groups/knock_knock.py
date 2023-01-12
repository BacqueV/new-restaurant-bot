from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp


@dp.message_handler(Command('knock_knock', prefixes='!/'))
async def knock_command(message: types.Message):
    await message.reply('По башке себе стучи, бля')
