# -*- coding: utf-8 -*-
from ..base_test_case import BaseTestCase
from ..mocks.aiogram import Dispatcher

from datetime import date, timedelta

from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager
from wakebot.processors import RuGeneral
from wakebot.processors.reserve import ReserveProcessor

from aiogram.types import Message, CallbackQuery, Chat, User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ReserveProcessorTestCase(BaseTestCase):
    "ReserveProcessor class"

    def setUp(self):
        self.strings = RuGeneral

        self.chat = Chat()
        self.chat.id = 101
        self.user = User()
        self.user.id = 111

        dp = Dispatcher()
        self.data_adapter = MemoryDataAdapter()
        self.state_manager = StateManager(self.data_adapter)
        self.processor = ReserveProcessor(dp, self.state_manager, self.strings)

        message = Message()
        message.chat = self.chat
        message.from_user = self.user
        message.message_id = 121
        message.text = "Some text"
        message.answer = self.answer_mock
        message.edit_text = self.edit_text_mock
        self.test_message = message

        callback = CallbackQuery()
        callback.answer = self.callback_answer_mock
        callback.message = message
        self.test_callback_query = callback

    async def answer_mock(self, text, parse_mode=None, reply_markup=None):
        self.message = Message()
        self.message.text = text
        self.message.reply_markup = reply_markup

    async def callback_answer_mock(self, text):
        self.callback_answer_text = text

    async def edit_text_mock(self, text, parse_mode=None, reply_markup=None):
        await self.answer_mock(text, parse_mode, reply_markup)

    def append_state(self, key, state_type="*", state="*"):
        state_data = {}
        state_data["state_type"] = state_type
        state_data["state"] = state
        self.data_adapter.append_data(key, state_data)

    def create_main_text(self):
        return "Hello message!"

    def create_book_text(self):
        return "Reserve Book menu message text"

    def create_list_text(self):
        return "Reserve List menu message text"

    def create_main_keyboard(self):
        """Create Main menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=1)

        button = InlineKeyboardButton(self.strings.reserve.start_book_button,
                                      callback_data='book')
        result.add(button)
        button = InlineKeyboardButton(self.strings.reserve.list_button,
                                      callback_data='list')
        result.add(button)

        return result

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

        # Adding Back-button separately
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_list_keyboard(self):
        """Create List menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_date_keyboard(self):
        """Create Date menu InlineKeyboardMarkup"""

        now = date.today()
        result = InlineKeyboardMarkup(row_width=3)

        buttons = [InlineKeyboardButton(
                   (now + timedelta(i)).strftime(self.strings.date_format),
                   callback_data=str(i))
                   for i in range(6)]

        result.add(*buttons)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_hour_keyboard(self, start=9, count=15, row_width=5):
        """Create Hour menu InlineKeyboardMarkup"""

        result = InlineKeyboardMarkup(row_width=row_width)

        buttons = [InlineKeyboardButton(f"{start + i}:", callback_data=str(i))
                   for i in range(count)]

        result.add(*buttons)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_minute_keyboard(self, step=5, row_width=6):
        """Create Hour menu InlineKeyboardMarkup"""

        result = InlineKeyboardMarkup(row_width=row_width)

        buttons = [InlineKeyboardButton(f"{i}", callback_data=str(i))
                   for i in range(0, 60, step)]

        result.add(*buttons)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    async def test_callback_main_book(self):
        """Proceed press Book button in Main menu"""
        callback = self.test_callback_query
        callback.data = "book"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "main")

        checked = self.processor.check_filter(callback, "reserve", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_query_main(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_book_back(self):
        """Proceed press Back button in Book menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_main_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(callback, "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_book(callback)

        self.check_state(state_key, self.create_main_text(),
                         reply_markup, "reserve", "main")

    async def test_callback_book_date(self):
        """Proceed press Date button in Book menu"""
        callback = self.test_callback_query
        callback.data = "date"
        reply_markup = self.create_date_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(callback, "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "date")

    async def test_callback_date_back(self):
        """Proceed press Back button in Date menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "date")

        checked = self.processor.check_filter(callback, "reserve", "date")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_date(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_book_time(self):
        """Proceed press Time button in Book menu"""
        callback = self.test_callback_query
        callback.data = "time"
        reply_markup = self.create_hour_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(callback, "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "hour")

    async def test_callback_hour_back(self):
        """Proceed press Back button in Hour menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "hour")

        checked = self.processor.check_filter(callback, "reserve", "hour")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_hour(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_minute(self):
        """Proceed choose hour in Hour menu"""
        callback = self.test_callback_query
        callback.data = "18"
        reply_markup = self.create_minute_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "hour")

        checked = self.processor.check_filter(callback, "reserve", "hour")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_hour(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "minute")

    async def test_callback_minute_back(self):
        """Proceed press Back button in Minute menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_hour_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "minute")

        checked = self.processor.check_filter(callback, "reserve", "minute")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_minute(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "hour")

    async def test_callback_main_list(self):
        """Proceed press List button in Main menu"""
        callback = self.test_callback_query
        callback.data = "list"
        reply_markup = self.create_list_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "main")

        checked = self.processor.check_filter(callback, "reserve", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_query_main(callback)

        self.check_state(state_key, self.create_list_text(),
                         reply_markup, "reserve", "list")

    async def test_callback_list_back(self):
        """Proceed press Back button in List menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_main_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "list")

        checked = self.processor.check_filter(callback, "reserve", "list")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_query_list(callback)

        self.check_state(state_key, self.create_main_text(),
                         reply_markup, "reserve", "main")

    def check_state(self, key, text, reply_markup,
                    state_type=None, state=None):
        """A util method to check current state"""

        state_data = self.data_adapter.get_data_by_keys(key)

        passed, alert = self.assert_params(self.message.text, text)
        assert passed, alert
        passed, alert = self.assert_params(self.message.reply_markup,
                                           reply_markup)
        assert passed, alert
        if state_type:
            passed, alert = self.assert_params(state_data["state_type"],
                                               state_type)
        assert passed, alert
        passed, alert = self.assert_params(state_data["state"], state)
        assert passed, alert


if __name__ == "__main__":
    ReserveProcessorTestCase().run_tests_async()
