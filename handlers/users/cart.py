from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import dp, db
from states.main import ShopState
from keyboards.default.main_menu import btn_back, btn_order


@dp.message_handler(text='Корзинка', state='*')
async def get_cart_items(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    items = db.get_all_items(cart_id=cart_id)

    if items:

        text = '<b>Ваши заказы</b>\n\n'
        markup_orders = ReplyKeyboardMarkup(
            row_width=2,
            resize_keyboard=True
        )

        for name, quantity, price in items:
            text += f"Блюдо: {db.get_data(id=name)[1]}\n" \
                    f"Количество: {quantity} шт.\n" \
                    f"Общая цена: {price}$\n\n"

            meal_id = db.get_data(id=name)[0]
            await state.update_data({'meal_id': meal_id})

            markup_orders.insert(KeyboardButton(
                text=f'❌ {db.get_data(id=name)[1]} ❌',
                callback_data=f'{meal_id}'
                )
            )

        markup_orders.row(KeyboardButton(
            text='Удалить все'
            ), btn_back, btn_order
        )
        await message.answer(text, reply_markup=markup_orders)
        await ShopState.cart.set()
    else:
        await message.answer('Заказов нет, стоило бы исправить! 😅')
        await ShopState.category.set()
