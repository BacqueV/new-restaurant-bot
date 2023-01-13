from loader import dp, bot
from data.config import CHANNELS
from utils.misc import subscription
from aiogram import types
from keyboards.inline.subscription import markup_sub
from keyboards.default.main_menu import markup_categories
from states.main import ShopState


@dp.callback_query_handler(text='check_sub')
async def checker(call: types.CallbackQuery):
    name = call.from_user.full_name
    await call.answer('Проверка подписки')
    result = str()
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)

        if status:
            final_status *= status
            result += f"✅ <b>{channel.title}</b> -- подписан!\n\n"
        else:
            final_status *= False
            invite_link = await channel.export_invite_link()
            result += f"🙅‍ <a href='{invite_link}'><b>{channel.title}</b></a> -- не подписан!\n\n"

    await call.message.delete()
    if final_status:
        text = f"Добро пожаловать, {name}!"
        await ShopState.category.set()
        await call.message.answer(text, reply_markup=markup_categories)
    else:
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=markup_sub)
