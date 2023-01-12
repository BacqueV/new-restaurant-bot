import asyncio

import aiogram.utils.exceptions
import pandas as pd
from aiogram import types

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(text="/allusers", user_id=ADMINS, state='*')
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
        await bot.send_message(message.chat.id, df)


@dp.message_handler(text="/advert", user_id=ADMINS, state='*')
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        try:
            await bot.send_message(chat_id=user_id, text="@ssnizhonka subscribe this channel!")
        except aiogram.utils.exceptions.BotBlocked:
            pass
        await asyncio.sleep(0.05)


@dp.message_handler(text="/cleandb", user_id=ADMINS, state='*')
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.reply("DB cleaned!")
