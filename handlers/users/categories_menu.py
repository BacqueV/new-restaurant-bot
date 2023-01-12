from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu import make_meals_markup
from loader import dp, db
from states.main import ShopState


@dp.message_handler(state=ShopState.category)
async def get_meals_by_category(message: types.Message, state: FSMContext):
    category_name = message.text
    category_id = db.get_category(name=category_name)[0]
    await state.update_data({
        'category_id': category_id
    })
    markup_meals = make_meals_markup(category_id)

    await state.update_data({
        'category_name': category_name
    })
    await message.answer(f"Категория: <b>{category_name}</b>",
                         reply_markup=markup_meals)
    await ShopState.next()
