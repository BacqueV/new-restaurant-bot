from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu import numbers
from loader import dp, db
from states.main import ShopState


@dp.message_handler(state=ShopState.meal_info)
async def buying_meal(message: types.Message, state: FSMContext):
    meal_name = message.text
    description = db.get_data(name=meal_name)[2]
    price = db.get_data(name=meal_name)[-1]

    msg = f"<i>{meal_name.title()}</i> — {price}$\n\n" \
          f"{description}"
    await state.update_data({
        'meal_name': meal_name,
        'meal_price': int(price)
    })
    await message.answer(msg, reply_markup=numbers)
    await ShopState.next()
