import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsPrivate
from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.subscription import markup_sub
from data.config import CHANNELS
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.from_user.full_name
    username = message.from_user.username

    channels_format = str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f"▶️ <a href='{invite_link}'><b>{chat.title}</b></a>\n"

    text = f"<b>Subscribe this channels</b>\n\n" \
           f"{channels_format}"

    # Adding user into DB
    try:
        db.add_user(id=message.from_user.id,
                    username=username,
                    name=name)
        await message.answer(text, reply_markup=markup_sub)
        db.add_user_cart(user_id=message.from_user.id)

        # Informing admins
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} joined to DB.\nThere are {count} users in DB."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} is already in DB")
        await message.answer(text, reply_markup=markup_sub)
