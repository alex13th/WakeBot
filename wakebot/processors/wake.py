# -*- coding: utf-8 -*-
from aiogram.types import Message, ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher

from wakebot.adapters.state import StateManager
from wakebot.processors.reserve import ReserveProcessor
from ..entities.user import User
from typing import Union
from ..entities.wake import Wake, ReserveSetType


class WakeProcessor(ReserveProcessor):
    """Proceed a wake reservaion process

    Attributes:
        dispatcher:
            A telegram bot dispatcher instance instance.
        state_manager:
            A state manager class instance
        strings:
            A locale strings class
        book_handlers:
            A dictionary of book menu handlers.
            A key matches InlineKeyboardButton.data value of book menu.
            A value must contain handler function - f().
    """

    def __init__(self,
                 dispatcher: Dispatcher,
                 state_manager: StateManager,
                 strings: any,
                 state_type: Union[str, int, None] = "wake",
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
        super().__init__(dispatcher, state_manager, strings,
                         state_type=state_type, parse_mode=parse_mode)

        self.reserve_set_types["set"] = ReserveSetType("set", 10)

        dispatcher.register_message_handler(self.cmd_wake, commands=["wake"])

    async def cmd_wake(self, message: Message):
        """Proceed /wake command"""

        text, reply_markup, state, _ = self.create_main_message()

        answer = await message.answer(
            self.strings.wake.hello_message,
            reply_markup=self.create_main_keyboard(),
            parse_mode=self.parse_mode)

        self.update_state(answer, message_state=True)
        state_manager = self.state_manager

        reserve = self.create_reserve(answer)

        from_user = message.from_user
        user = User(from_user.first_name, from_user.last_name,
                    displayname=from_user.full_name, telegram_id=from_user.id)
        reserve.user = user

        state_manager.set_state(state_type="wake", state="main", data=reserve)

    def create_main_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """

        return self.strings.wake.hello_message

    def create_book_text(self, show_contact: bool = True) -> str:
        """Create a book menu text

        Returns:
            A message text.
        """

        reserve = self.state_manager.data
        result = (f"{self.strings.reserve.type_label} "
                  f"{self.strings.wake.wake_text}\n")

        if reserve.user:
            result += f"{self.strings.name_label} {reserve.user.displayname}\n"
            if show_contact and reserve.user.phone_number:
                result += (f"{self.strings.phone_label} "
                           f"{reserve.user.phone_number}\n")

        result += (f"{self.strings.reserve.date_label} "
                   f"{reserve.start_date.strftime(self.strings.date_format)}"
                   "\n")

        if reserve.start_time:
            start_time = reserve.start_time.strftime(self.strings.time_format)
            result += (f"{self.strings.reserve.start_label} "
                       f"{start_time}\n")
            end_time = reserve.end_time.strftime(self.strings.time_format)
            result += (f"{self.strings.reserve.end_label} "
                       f"{end_time}\n")

        result += (f"{self.strings.reserve.set_type_label} "
                   f"{self.strings.reserve.set_types[reserve.set_type.set_id]}"
                   f" ({reserve.set_count})\n")

        return result

    def create_list_text(self) -> str:
        """Create list menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """
        return "Wake List menu message text"

    def create_book_keyboard(self) -> InlineKeyboardMarkup:
        """Create book menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """
        result = InlineKeyboardMarkup(row_width=1)

        # Adding Date- and Time- buttons by a row for each
        button = InlineKeyboardButton(self.strings.date_button,
                                      callback_data='date')
        result.add(button)
        button = InlineKeyboardButton(self.strings.time_button,
                                      callback_data='time')
        result.add(button)

        # Adding Set- and Hour- buttons in one row
        set_button = InlineKeyboardButton(self.strings.wake.set_button,
                                          callback_data='set')
        hour_button = InlineKeyboardButton(self.strings.wake.hour_button,
                                           callback_data='set_hour')
        result.row(set_button, hour_button)

        # Adding Board- and Hydro- buttons in one row
        set_button = InlineKeyboardButton(self.strings.wake.board_button,
                                          callback_data='wake')
        hour_button = InlineKeyboardButton(self.strings.wake.hydro_button,
                                           callback_data='hydro')
        result.row(set_button, hour_button)

        button = InlineKeyboardButton(self.strings.phone_button,
                                      callback_data='phone')
        result.add(button)

        if self.state_manager.data:
            reserve: Wake = self.state_manager.data
            if reserve.is_complete:
                button = InlineKeyboardButton(
                    self.strings.reserve.apply_button,
                    callback_data='apply')
                result.add(button)

        # Adding Back-button separately
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_reserve(self, message: Message) -> Wake:
        """Create new Reserve instance
        An update_state method call this when state hasn't an reservation data.

        Returns:
            An Wake class or child class instance .
        """
        result = Wake()

        from_user = message.from_user
        user = User(from_user.first_name, from_user.last_name,
                    displayname=from_user.full_name, telegram_id=from_user.id)
        result.user = user

        return result
