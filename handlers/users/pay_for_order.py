from utils.misc.product import Product
from loader import dp, db, bot
from aiogram import types
from states.main import ShopState
from aiogram.types import LabeledPrice
from data.shipping import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from data.config import ADMINS
from keyboards.default.main_menu import categories


@dp.message_handler(text='Заказать', state=ShopState.cart)
async def order_meal(message: types.Message):

    user_id = message.from_user.id
    user_cart_id = db.select_cart(user_id=user_id)[0]
    items = db.get_all_items(cart_id=user_cart_id)

    msg = str()
    prices = list()
    for item in items:
        data = db.get_data(id=item[0])
        name = data[1]
        price = int(data[-2])
        amount = item[-2]
        msg += f"{name} ({price}) x {amount} = {(amount * price)}, "
        prices.append(
            LabeledPrice(label=name, amount=int(price * amount * 100))
        )

    products = Product(
        title='Пора платить по счетам!',
        description=msg[:-2],
        start_parameter='create_invoice_order',
        currency='UZS',
        prices=prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True
    )

    await bot.send_invoice(
        chat_id=user_id,
        **products.generate_invoice(),
        payload=f'payload:order_user_id{user_id}'
    )

    db.delete_data_user(cart_id=user_cart_id)


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Доставка только на территории Узбекистана!")
    elif query.shipping_address.city.lower() == "urganch":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Спасибо за покупку!", reply_markup=categories)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Проданный материал: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Пользователь Телеграм: {pre_checkout_query.from_user.first_name}\n"
                                f"Продавец: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}")
