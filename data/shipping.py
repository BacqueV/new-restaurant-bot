from aiogram import types
from aiogram.types import LabeledPrice

REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title="emu (3 дня)",
    prices=[
        LabeledPrice(
            'Спец. упаковка', 500000),
        LabeledPrice(
            'Доставка за 3 рабочих дня', 5000000),
    ]
)
FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Экспресс почта (1 день)',
    prices=[
        LabeledPrice(
            'Доставка за 1 день', 7000000),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(
    id='pickup',
    title="Забрать самому",
    prices=[
        LabeledPrice("Без доставки", -5000000)
    ]
)
