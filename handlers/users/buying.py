from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.main import ShopState
from keyboards.default.main_menu import markup_categories


@dp.message_handler(state=ShopState.buying)
async def get_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    meal_name = data.get('meal_name')
    price = data.get('meal_price')

    try:
        amount = int(message.text)
        if int(amount) >= 1:
            await message.answer(f"<code>{meal_name} x {amount} = {price * amount}</code>",
                                 reply_markup=markup_categories)
            await ShopState.category.set()
        else:
            await message.reply('Введите количество корректно')
    except ValueError:
        await message.reply('Введите количество корректно')
