from aiogram import types
from states.main import ShopState
from loader import dp
from keyboards.default.main_menu import markup_categories
from filters import IsPrivate


@dp.message_handler(IsPrivate(), text='Меню', state='*')
async def menu_commands(message: types.Message):
    await message.answer('<i>Выберите блюдо на вечер...</i>', reply_markup=markup_categories)
    await ShopState.category.set()
