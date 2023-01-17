from loader import db, dp
from aiogram import types
from states.main import ShopState
from keyboards.default.get_data import markup_send_number, markup_send_location
from keyboards.default.main_menu import markup_categories
from aiogram.dispatcher import FSMContext


@dp.message_handler(text='Настройки', state='*')
async def order_it(message: types.Message):

    await message.answer(
        f'Отправьте мне свои данные\n',
        reply_markup=markup_send_number
    )
    await ShopState.order.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=ShopState.order)
async def get_number(message: types.Message, state: FSMContext):
    phone_number = str(message.contact.phone_number)
    user_id = message.from_user.id

    await state.update_data(
        {
            'phone_number': phone_number,
            'user_id': user_id
        }
    )
    await message.answer('Номер сохранен!', reply_markup=markup_send_location)


@dp.message_handler(content_types=types.ContentType.LOCATION, state=ShopState.order)
async def get_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data['phone_number']
    user_id = data['user_id']

    lat = message.location.latitude
    lon = message.location.longitude

    have_number = db.check_existence_number()
    if have_number:
        db.update_order_data(number=phone_number, lat=lat, lon=lon, user_id=user_id)
    else:
        db.add_order(user_id=user_id, number=phone_number, lat=lat, lon=lon)
    await message.answer('Данные обновлены!', reply_markup=markup_categories)


@dp.message_handler(text='Выслать данные!', state=ShopState.order)
async def end_ordering(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        phone_number = data['phone_number']
        user_id = data['user_id']

        have_number = db.check_existence_number(id=user_id)
        if have_number:
            db.update_order_data(number=phone_number, lat='NULL', lon='NULL', user_id=user_id)
        else:
            db.add_order(user_id=user_id, number=phone_number, lat='NULL', lon='NULL')

        await message.answer(
            text='Данные обновлены!',
            reply_markup=markup_categories
        )
        await ShopState.category.set()
    except KeyError:
        await message.reply('Отправьте хотя бы номер вашего телефона!')
