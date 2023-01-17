from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.main_menu import markup_categories, btn_back, btn_settings
from loader import dp, db
from states.main import ShopState


@dp.message_handler(text='Удалить все', state=ShopState.cart)
async def clear_cart(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]

    db.delete_data(cart_id=cart_id)
    await message.answer(
        'Корзинка пуста, но я помогу вам набрать туда вещей!',
        reply_markup=markup_categories)
    await state.finish()


@dp.message_handler(state=ShopState.cart)
async def delete_meal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]

    meal = message.text.split()[1]
    meal_id = db.get_data(name=meal)[0]

    db.delete_data_user(cart_id=cart_id, product_id=meal_id)
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
            ), btn_back, btn_settings
        )
        await message.answer(text, reply_markup=markup_orders)
    else:
        await message.answer(
            'Заказов нет, стоило бы исправить! 😅',
            reply_markup=markup_categories
        )
        await ShopState.category.set()
