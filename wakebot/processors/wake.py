# -*- coding: utf-8 -*-
from aiogram.types import Message, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher

from wakebot.adapters.state import StateManager
from wakebot.processors.reserve import ReserveProcessor


class WakeProcessor(ReserveProcessor):
    """Proceed a wake reservaion process

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
                 state_type="wake",
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
                Default value: "wake"
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        super().__init__(dispatcher, state_manager, strings, state_type,
                         parse_mode)

        dispatcher.register_message_handler(self.cmd_wake, commands=["wake"])

    async def cmd_wake(self, message: Message):
        "Proceed /wake command"
        text, reply_markup, state, _ = self.create_main_message()

        self.update_state(message)
        state_manager = self.state_manager
        await message.answer(self.strings.wake.hello_message,
                             reply_markup=self.create_main_keyboard(),
                             parse_mode=self.parse_mode)

        state_manager.set_state(state_type="wake", state="main")

    def create_main_text(self):
        return self.strings.wake.hello_message

    def create_book_text(self):
        return "Wake Book menu message text"

    def create_list_text(self):
        return "Wake List menu message text"

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
