from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.main_menu import btn_back

btn_send_number = KeyboardButton(
    text='Отправить номер',
    request_contact=True
)
btn_send_location = KeyboardButton(
    text='Отправить локацию',
    request_location=True
)
btn_send_data = KeyboardButton(
    text='Выслать данные!'
)

markup_send_number = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
).add(
    btn_send_number
).add(
    btn_send_data,
    btn_back
)

markup_send_location = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
).add(
    btn_send_location
).add(
    btn_send_data,
    btn_back
)
