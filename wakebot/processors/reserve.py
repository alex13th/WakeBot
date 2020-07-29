# -*- coding: utf-8 -*-
from datetime import date, timedelta

from aiogram.dispatcher import Dispatcher
from aiogram.types import CallbackQuery, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from wakebot.adapters.state import StateManager
from wakebot.processors.common import StatedProcessor


class ReserveProcessor(StatedProcessor):
    """Proceed a reservaion process

    Attributes:
        strings:
            A locale strings class
        state_manager:
            A state manager class instance
    """

    def __init__(self,
                 dispatcher: Dispatcher,
                 state_manager: StateManager,
                 strings,
                 state_type="reserve",
                 parse_mode=ParseMode.MARKDOWN):
        """Initialize a class instance

        Args:
            dispatcher:
                A telegram bot dispatcher instance instance.
            state_manager:
                A state manager class instance
            strings:
                A locale strings class.
            state_type:
                Optional, A default state type.
                Default value: "reserve"
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        super().__init__(dispatcher, state_manager, state_type, parse_mode)
        self.strings = strings

        self.register_callback_query_handler(self.callback_query_main, "main")
        self.register_callback_query_handler(self.callback_query_list, "list")
        self.register_callback_query_handler(self.callback_query_book, "book")
        self.register_callback_query_handler(self.callback_query_date, "date")
        self.register_callback_query_handler(self.callback_query_hour, "hour")
        self.register_callback_query_handler(self.callback_query_minute,
                                             "minute")

    async def callback_query_main(self, callback_query: CallbackQuery):
        """Proceed Main menu buttons"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "book":
            text, reply_markup, state, answer = self.create_book_message()

        elif callback_query.data == "list":
            text, reply_markup, state, answer = self.create_list_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_query_book(self, callback_query: CallbackQuery):
        """Proceed Book menu buttons"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_main_message()

        if callback_query.data == "date":
            text, reply_markup, state, answer = self.create_date_message()

        if callback_query.data == "time":
            text, reply_markup, state, answer = self.create_hour_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_query_date(self, callback_query: CallbackQuery):
        """Proceed Date menu buttons"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_book_message()
        else:
            text, reply_markup, state, answer = self.create_book_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_query_hour(self, callback_query: CallbackQuery):
        """Proceed Hour menu buttons"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_book_message()
        else:
            text, reply_markup, state, answer = self.create_minute_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_query_minute(self, callback_query: CallbackQuery):
        """Proceed Minute menu buttons"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_hour_message()
        else:
            text, reply_markup, state, answer = self.create_book_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_query_list(self, callback_query: CallbackQuery):
        """Proceed Main menu buttons"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_main_message()

        elif callback_query.data == "book":
            text, reply_markup, state, answer = self.create_book_message()

        elif callback_query.data == "list":
            text, reply_markup, state, answer = self.create_list_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    def create_main_message(self):
        text = self.create_main_text()
        reply_markup = self.create_main_keyboard()
        state = "main"
        answer = text

        return (text, reply_markup, state, answer)

    def create_book_message(self):
        text = self.create_book_text()
        reply_markup = self.create_book_keyboard()
        state = "book"
        answer = text

        return (text, reply_markup, state, answer)

    def create_list_message(self):
        text = self.create_list_text()
        reply_markup = self.create_list_keyboard()
        state = "list"
        answer = text

        return (text, reply_markup, state, answer)

    def create_date_message(self):
        text = self.create_book_text()
        reply_markup = self.create_date_keyboard()
        state = "date"
        answer = text

        return (text, reply_markup, state, answer)

    def create_hour_message(self):
        text = self.create_book_text()
        reply_markup = self.create_hour_keyboard()
        state = "hour"
        answer = text

        return (text, reply_markup, state, answer)

    def create_minute_message(self):
        text = self.create_book_text()
        reply_markup = self.create_minute_keyboard()
        state = "minute"
        answer = text

        return (text, reply_markup, state, answer)

    def create_main_text(self):
        return "Hello message!"

    def create_book_text(self):
        return "Reserve Book menu message text"

    def create_list_text(self):
        return "Reserve List menu message text"

    def create_main_keyboard(self):
        """Create main menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=1)

        button = InlineKeyboardButton(self.strings.reserve.start_book_button,
                                      callback_data='book')
        result.add(button)
        button = InlineKeyboardButton(self.strings.reserve.list_button,
                                      callback_data='list')
        result.add(button)

        return result

    def create_list_keyboard(self):
        """Create list menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_book_keyboard(self):
        """Create book menu InlineKeyboardMarkup"""
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
