from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # set default commands
    await set_default_commands(dispatcher)

    # creating db
    try:
        db.create_table_orders()
        db.create_table_users()
        db.create_categories()
        db.create_table_meals()
        db.create_table_cart()
        db.create_table_cart_items()
    except Exception as err:
        print(err)

    # informing admins
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
