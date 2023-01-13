from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db


@dp.message_handler(text='Корзинка', state='*')
async def get_cart_items(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]

    items = db.get_all_items(cart_id=cart_id)

    if cart_id is not None:

        text = '<b>Ваши заказы</b>\n\n'
        markup_orders = InlineKeyboardMarkup(row_width=1)

        for name, quantity, price in items:
            text += f"Блюдо: {db.get_data(id=name)[1]}\n" \
                    f"Количество: {quantity} шт.\n" \
                    f"Общая цена: {price}$\n\n"

            markup_orders.row(InlineKeyboardButton(
                text=f'❌ {db.get_data(id=name)[1]} ❌',
                callback_data='sad'
                )
            )

        markup_orders.row(InlineKeyboardButton(
            text='Удалить все',
            callback_data='delete_add'
            )
        )
        await message.answer(text, reply_markup=markup_orders)
    else:
        await message.answer('Вы еще ничего у нас не заказали')
