from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_subscription = InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')
markup_sub = InlineKeyboardMarkup().insert(btn_subscription)
