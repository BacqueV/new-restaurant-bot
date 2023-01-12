from loader import dp
from .throttling import ThrottlingMiddleware
from .is_subscribed import BigBrother

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrother())
