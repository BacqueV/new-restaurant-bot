from aiogram import types
from states.main import ShopState
from loader import dp, db
from keyboards.default.main_menu import markup_categories
from filters import IsPrivate
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsPrivate(), text='Меню', state='*')
async def menu_commands(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]

    await state.update_data({'cart_id': cart_id})
    await message.answer('<i>Выберите блюдо на вечер...</i>', reply_markup=markup_categories)

    await ShopState.category.set()
