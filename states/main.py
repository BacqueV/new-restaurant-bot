from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopState(StatesGroup):
    main_menu = State()
    category = State()
    meal_info = State()
    buying = State()
