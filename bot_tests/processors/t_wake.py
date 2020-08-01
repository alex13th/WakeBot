# -*- coding: utf-8 -*-
from ..mocks.aiogram import Dispatcher
from ..processors.t_reserve import ReserveProcessorTestCase

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager
from wakebot.processors import RuGeneral
from wakebot.processors.wake import WakeProcessor


class WakeProcessorTestCase(ReserveProcessorTestCase):
    "WakeProcessor class"

    def setUp(self):
        super().setUp()
        self.strings = RuGeneral

        dp = Dispatcher()
        self.data_adapter = MemoryDataAdapter()
        self.state_manager = StateManager(self.data_adapter)
        self.processor = WakeProcessor(dp, self.state_manager, self.strings)

    def append_state(self, key, state_type="*", state="*"):
        state_data = {}
        state_data["state_type"] = state_type
        state_data["state"] = state
        self.data_adapter.append_data(key, state_data)

    def create_book_keyboard(self):
        """Create Book menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=1)

        # Adding Date- and Time- buttons by a row for each
        button = InlineKeyboardButton(self.strings.date_button,
                                      callback_data='date')
        result.add(button)
        button = InlineKeyboardButton(self.strings.time_button,
                                      callback_data='time')
        result.add(button)

        # Adding Set- and Hour- buttons in one row
        set_button = InlineKeyboardButton(self.strings.reserve.set_button,
                                          callback_data='set')
        hour_button = InlineKeyboardButton(self.strings.reserve.hour_button,
                                           callback_data='hour')
        result.row(set_button, hour_button)

        # Adding Back-button separately
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_main_text(self):
        return self.strings.wake.hello_message

    def create_book_text(self):
        return "Wake Book menu message text"

    def create_list_text(self):
        return "Wake List menu message text"

    async def test_cmd_wake(self):
        """Proceed /wake command"""
        message = self.test_message
        message.text = "/wake"
        reply_markup = self.create_main_keyboard()

        await self.processor.cmd_wake(message)
        state_data = self.data_adapter.get_data_by_keys('101-111-121')

        passed, message = self.assert_params(self.message.text,
                                             RuGeneral.wake.hello_message)
        assert passed, message

        passed, message = self.assert_params(self.message.reply_markup,
                                             reply_markup)
        assert passed, message

        passed, message = self.assert_params(state_data["state_type"], "wake")
        assert passed, message

        passed, message = self.assert_params(state_data["state"], "main")
        assert passed, message

    async def test_callback_main_book(self):
        """Proceed press Book button in Main menu"""
        callback = self.test_callback_query
        callback.data = "book"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "main")

        checked = self.processor.check_filter(callback, "wake", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_query_main(callback)

        self.check_state(state_key, "Wake Book menu message text",
                         reply_markup, "wake", "book")

    async def test_callback_main_list(self):
        """Proceed press List button in Main menu"""
        callback = self.test_callback_query
        callback.data = "list"
        reply_markup = self.create_list_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "main")

        checked = self.processor.check_filter(callback, "wake", "main")
        passed, message = self.assert_params(checked, True)

        await self.processor.callback_query_main(callback)

        self.check_state(state_key, "Wake List menu message text",
                         reply_markup, "wake", "list")

    async def test_callback_book_date(self):
        """Proceed press Date button in Book menu"""
        callback = self.test_callback_query
        callback.data = "date"
        reply_markup = self.create_date_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "main")

        checked = self.processor.check_filter(callback, "wake", "book")
        passed, message = self.assert_params(checked, True)

        await self.processor.callback_query_book(callback)

        self.check_state(state_key, "Wake Book menu message text",
                         reply_markup, "wake", "date")


if __name__ == "__main__":
    WakeProcessorTestCase().run_tests_async()
