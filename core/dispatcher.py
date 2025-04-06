from aiogram import Dispatcher
from handlers import commands, callbacks
from middlewares.subscription import SubscriptionMiddleware

dp = Dispatcher()

# Регистрация middleware
dp.callback_query.middleware(SubscriptionMiddleware())
dp.message.middleware(SubscriptionMiddleware())

# Регистрация роутеров
dp.include_router(commands.router)
dp.include_router(callbacks.router)