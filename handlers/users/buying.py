from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu import markup_categories
from loader import dp, db
from states.main import ShopState


@dp.message_handler(state=ShopState.buying)
async def get_amount(message: types.Message, state: FSMContext):

    data = await state.get_data()

    meal_name = data.get('meal_name')
    price = data.get('meal_price')

    meal_id = db.get_data(name=meal_name)[0]
    cart_id = db.select_cart(user_id=message.from_user.id)[0]

    await state.update_data({'cart_id': cart_id})

    try:
        amount = int(message.text)
        if amount >= 1:
            meals = db.check_existence(product_id=meal_id, cart_id=cart_id)
            if meals:
                previous_quantity = meals[2]

                db.update_cart_data(
                    quantity=amount + previous_quantity,
                    cost=float(price * (amount + previous_quantity)),
                    product_id=meal_id,
                    cart_id=cart_id
                )

                await message.answer('Данные обновлены!', reply_markup=markup_categories)
            else:
                db.add_cart_item(product_id=meal_id, quantity=amount, cost=float(price * amount), cart_id=cart_id)
                await message.answer(f"<code>{meal_name} x {amount} = {float(price * amount)}$</code>",
                                     reply_markup=markup_categories)
            await ShopState.category.set()
        else:
            await message.reply('Введите количество корректно')
    except ValueError:
        await message.reply('Введите количество корректно')
