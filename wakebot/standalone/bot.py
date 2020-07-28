from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from wakebot.adapters.state import StateProvider
from wakebot.adapters.data import MemoryDataAdapter
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

ma = MemoryDataAdapter()
sp = StateProvider(ma)


@dp.message_handler(commands=["wake"])
@sp.message_state("")
async def cmd_wake(message, state_manager=None):
    state_manager.set_state(state_type="wake",
                            message_id=message.message_id)
    await message.answer("WAKE COMMAND")


@dp.message_handler(commands=["start"])
@sp.message_state(state_type="wake")
async def cmd_start(message, state_manager=None):
    await message.answer("WAKE START")


if __name__ == "__main__":
    executor.start_polling(dp)
