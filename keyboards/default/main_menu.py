from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

# main menu
markup_main = ReplyKeyboardMarkup(resize_keyboard=True)
markup_main.row('Меню')
markup_main.row('Корзинка', 'Мои заказы')
markup_main.row('Настройки', 'Кошелек')

# meal menu
btn_back = KeyboardButton(text='Назад')
btn_cart = KeyboardButton(text='Корзинка')

categories = db.select_categories()

# mark up
markup_categories = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup_categories.add(
    btn_back, btn_cart
)


for category in categories:
    markup_categories.insert(KeyboardButton(text=category[1]))


def make_meals_markup(category_id):
    meals = db.select_all_meals(id=category_id)
    markup_meals = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup_meals.add(btn_back, btn_cart)
    for meal in meals:
        markup_meals.insert(KeyboardButton(text=meal[1]))
    return markup_meals


numbers = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
for number in range(1, 10):
    numbers.insert(KeyboardButton(text=str(number)))
numbers.add(btn_back)
