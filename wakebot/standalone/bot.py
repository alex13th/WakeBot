from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from wakebot.processors import RuGeneral
from wakebot.processors.default import DefaultProcessor
from wakebot.processors.wake import WakeProcessor
from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


state_manager = StateManager(MemoryDataAdapter())

default_processor = DefaultProcessor(dp, RuGeneral)
wake_processor = WakeProcessor(dp, state_manager, RuGeneral)

if __name__ == "__main__":
    executor.start_polling(dp)
