import asyncio
import datetime
import re

import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from filters import IsGroup, AdminFilter
from loader import dp, bot

msg_delete_time = 'Сообщение удалится через 5 секунд'


# handler for /ro oki !ro (read-only) commands
# putting user to read-only mode


@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"), AdminFilter())
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5

    """
    !ro 
    !ro 5 
    !ro 5 test
    !ro test
    !ro test test test
    /ro 
    /ro 5 
    /ro 5 test
    /ro test
    """
    # 5 - minutes mute
    # !ro 5
    # command='!ro' time='5' comment=[]

    # 50 minutes mute
    # !ro 50 ban for advertising
    # command='!ro' time='50' comment=['ban', 'for', 'advertisement']

    time = int(time)

    # Calculating ban time (current time + n minutes)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    try:
        user_allowed = types.ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_invite_users=False,
            can_change_info=False,
            can_pin_messages=False,
        )
        # await message.chat.restrict(
        # user_id=member_id,
        # can_send_messages=False,
        # can_send_media_messages=True,
        # until_date=until_date
        # )
        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=member_id,
                                       permissions=user_allowed, until_date=until_date)
        await message.reply_to_message.delete()
    except aiogram.utils.exceptions.BadRequest as err:
        await message.answer(f"Error! {err.args}")
        return

    if comment is not None:
        await message.answer(
            f"{message.reply_to_message.from_user.full_name} пошел обдумывать свое поведение на {time} минут.\n"
            f"Причина: \n<b>{comment}</b>"
        )
    else:
        await message.answer(
            f"{message.reply_to_message.from_user.full_name} пошел обдумывать свое поведение на {time} минут...")

    service_message = await message.reply(msg_delete_time)
    # deleting message after 5 seconds
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


# removing user from read-only mode


@dp.message_handler(IsGroup(), Command("unro", prefixes="!/"), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id

    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )
    service_message = await message.reply(msg_delete_time)

    await asyncio.sleep(5)
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    await message.reply(f"{member.full_name}, говори!")

    # deleting message
    await message.delete()
    await service_message.delete()


# Banning user (remove from chat)


@dp.message_handler(IsGroup(), Command("ban", prefixes="!/"), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    await message.chat.kick(user_id=member_id)

    await message.answer(f"{message.reply_to_message.from_user.full_name} получил по башке сапогом.")
    service_message = await message.reply(msg_delete_time)

    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


# unbanning user (he is able to join the group)
@dp.message_handler(IsGroup(), Command("unban", prefixes="!/"), AdminFilter())
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    await message.chat.unban(user_id=member_id)
    await message.answer(f"{message.reply_to_message.from_user.full_name} прощен.")
    service_message = await message.reply(msg_delete_time)

    await asyncio.sleep(5)

    await message.delete()
    await service_message.delete()
