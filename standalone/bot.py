import psycopg2
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from wakebot.processors.default import DefaultProcessor
from wakebot.processors import WakeProcessor, SupboardProcessor
from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager
from wakebot.adapters.postgres import PostgressWakeAdapter
from wakebot.adapters.postgres import PostgressSupboardAdapter
from wakebot.adapters.postgres import PostgresUserAdapter

from config import DefaultStrings, WakeStrings, SupboardStrings

TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


state_manager = StateManager(MemoryDataAdapter())

default_processor = DefaultProcessor(dp, DefaultStrings)
connection = psycopg2.connect(DATABASE_URL)
user_adapter = PostgresUserAdapter(connection, "wp38_users")

wake_adapter = PostgressWakeAdapter(connection, "wp38_wake")
wake_processor = WakeProcessor(dp,
                               state_manager=state_manager,
                               strings=WakeStrings,
                               data_adapter=wake_adapter,
                               user_data_adapter=user_adapter)

sup_adapter = PostgressSupboardAdapter(connection, "wp38_supboard")
sup_processor = SupboardProcessor(dp,
                                  state_manager=state_manager,
                                  strings=SupboardStrings,
                                  data_adapter=sup_adapter,
                                  user_data_adapter=user_adapter)
sup_processor.max_count = 6

if __name__ == "__main__":
    executor.start_polling(dp)
