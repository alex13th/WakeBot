import psycopg2
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from wakebot.processors import RuGeneral
from wakebot.processors.default import DefaultProcessor
from wakebot.processors.wake import WakeProcessor
from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager
from wakebot.adapters.postgres.wake import PostgressWakeAdapter
# from config import TOKEN

TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


state_manager = StateManager(MemoryDataAdapter())

default_processor = DefaultProcessor(dp, RuGeneral)
connection = psycopg2.connect(DATABASE_URL)

wake_adapter = PostgressWakeAdapter(connection)
wake_processor = WakeProcessor(dp, state_manager, RuGeneral, wake_adapter)

if __name__ == "__main__":
    executor.start_polling(dp)
