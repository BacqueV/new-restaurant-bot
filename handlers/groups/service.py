import io
from random import choice

from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsGroup
from filters.is_admin import AdminFilter
from loader import dp, bot

GREETING = ['Здорово', 'Привет', 'Здравствуй', 'Приветствую', 'Добро пожаловать']
GOODBYE = ['покинул нас', 'прощай', 'до встречи)', 'не скучай!', 'э ваще сьебался нахуй']


@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    greeting = choice(GREETING)
    members = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
    await message.reply(f"{greeting}, {members}.")


@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def banned_member(message: types.Message):
    goodbye = choice(GOODBYE)
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} покинул нас!")
    elif message.from_user.id == (await bot.me).id:
        return
    else:
        await message.answer(f"{message.left_chat_member.full_name} {goodbye}!\n"
                             f"От руки: {message.from_user.get_mention(as_html=True)}.")


@dp.message_handler(IsGroup(), Command("set_photo", prefixes="!/"), AdminFilter())
async def set_new_photo(message: types.Message):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_file = types.InputFile(photo)
    # 1- method
    await message.chat.set_photo(photo=input_file)


@dp.message_handler(IsGroup(), Command("set_title", prefixes="!/"), AdminFilter())
async def set_new_title(message: types.Message):
    source_message = message.reply_to_message
    title = source_message.text
    # 2- method
    await bot.set_chat_title(message.chat.id, title=title)


@dp.message_handler(IsGroup(), Command("set_description", prefixes="!/"), AdminFilter())
async def set_new_description(message: types.Message):
    source_message = message.reply_to_message
    description = source_message.text
    # 1- method
    # await bot.set_chat_description(message.chat.id, description=description)
    # 2- method
    await message.chat.set_description(description=description)
