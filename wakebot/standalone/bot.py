from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from wakebot.processors.default import DefaultProcessor
from wakebot.processors import RuStrings
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

default_processor = DefaultProcessor(dp, RuStrings)

if __name__ == "__main__":
    executor.start_polling(dp)
