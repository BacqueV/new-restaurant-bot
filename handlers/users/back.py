from aiogram import types
from loader import dp
from keyboards.default.main_menu import markup_main, markup_categories
from states.main import ShopState
from aiogram.dispatcher import FSMContext
from keyboards.default.main_menu import make_meals_markup


@dp.message_handler(text='Назад', state=ShopState.buying)
async def go_to_main(message: types.Message, state: FSMContext):

    data = await state.get_data()
    category_id = data['category_id']

    markup_meals = make_meals_markup(category_id)

    await ShopState.meal_info.set()
    await message.answer('Начнем!', reply_markup=markup_meals)


@dp.message_handler(text='Назад', state=ShopState.meal_info)
async def go_to_main(message: types.Message):
    await ShopState.category.set()
    await message.answer('Начнем!', reply_markup=markup_categories)


@dp.message_handler(text='Назад', state='*')
async def go_to_main(message: types.Message):
    await ShopState.category.set()
    await message.answer('Начнем!', reply_markup=markup_main)
