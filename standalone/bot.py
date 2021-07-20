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
DATABASE_URL = os.environ.get("DATABASE_URL")
board_count = os.environ.get("BOARD_COUNT")
hydro_count = os.environ.get("HYDRO_COUNT")
sup_count = os.environ.get("SUP_COUNT")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


state_manager = StateManager(MemoryDataAdapter())

default_processor = DefaultProcessor(dp, DefaultStrings)
connection = psycopg2.connect(DATABASE_URL)
user_adapter = PostgresUserAdapter(database_url=DATABASE_URL,
                                   table_name="wp38_users")

wake_adapter = PostgressWakeAdapter(database_url=DATABASE_URL,
                                    table_name="wp38_wake")
wake_processor = WakeProcessor(dp,
                               state_manager=state_manager,
                               strings=WakeStrings,
                               data_adapter=wake_adapter,
                               user_data_adapter=user_adapter)
wake_processor.logger_id = 586350636
wake_processor.board_count = int(board_count) if board_count else 5
wake_processor.hydro_count = int(hydro_count) if hydro_count else 10

sup_adapter = PostgressSupboardAdapter(database_url=DATABASE_URL,
                                       table_name="wp38_supboard")
sup_processor = SupboardProcessor(dp,
                                  state_manager=state_manager,
                                  strings=SupboardStrings,
                                  data_adapter=sup_adapter,
                                  user_data_adapter=user_adapter)
sup_processor.max_count = int(sup_count) if sup_count else 10
sup_processor.logger_id = 586350636

if __name__ == "__main__":
    executor.start_polling(dp)
