from typing import Union
from datetime import date, time, timedelta

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types import ForceReply, ReplyKeyboardRemove
from aiogram.types import KeyboardButton, InlineKeyboardButton

from wakebot.adapters.state import StateManager
from wakebot.processors.common import StatedProcessor
from ..entities.user import User
from ..entities.reserve import Reserve


class ReserveProcessor(StatedProcessor):
    """Proceed a reservaion process

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
                 state_type: Union[str, int, None] = "reserve",
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
                Optional. A default state type.
                Default value: "reserve"
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        super().__init__(dispatcher, state_manager, state_type, parse_mode)
        self.strings = strings

        self.register_callback_query_handler(self.callback_main, "main")
        self.register_callback_query_handler(self.callback_list, "list")
        self.register_callback_query_handler(self.callback_book, "book")
        self.register_callback_query_handler(self.callback_date, "date")
        self.register_callback_query_handler(self.callback_hour, "hour")
        self.register_callback_query_handler(self.callback_minute, "minute")
        self.register_message_handler(self.message_phone, state="phone")

        self.book_handlers = {}
        self.book_handlers["back"] = self.book_back
        self.book_handlers["date"] = self.book_date
        self.book_handlers["time"] = self.book_time
        self.book_handlers["phone"] = self.book_phone

    async def message_phone(self, message: Message):
        """Phone number reply message handler"""

        reserve = self.state_manager.data
        reserve.user.phone_number = message.text
        self.state_manager.finish()

        await message.answer(text=self.strings.phone_success_message,
                             reply_markup=ReplyKeyboardRemove())

        text, reply_markup, state, answer = self.create_book_message()
        answer = await message.answer(text, reply_markup=reply_markup,
                                      parse_mode=self.parse_mode)
        await message.reply_to_message.delete()
        await message.delete()

        self.update_state(answer, message_state=True)
        state_manager = self.state_manager

        state_manager.set_state(
            state_type=self.state_type,
            state=state,
            data=reserve)

    async def callback_main(self, callback_query: CallbackQuery):
        """Main menu CallbackQuery handler"""
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

    async def callback_book(self, callback_query: CallbackQuery):
        """Book menu CallbackQuery handler"""
        # State manager updated by StatedProcessor.check_filter method
        await self.book_handlers[callback_query.data](callback_query)

    async def callback_date(self, callback_query: CallbackQuery):
        """Date menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_book_message()
        elif callback_query.data.isdigit():
            start_date = date.today() + timedelta(int(callback_query.data))
            self.state_manager.data.start_date = start_date
            text, reply_markup, state, answer = self.create_book_message()
        else:
            await callback_query.answer(self.strings.callback_error)
            return

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_hour(self, callback_query: CallbackQuery):
        """Hour menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_book_message()
        elif callback_query.data.isdigit():
            if self.state_manager.data.start_time:
                minute = self.state_manager.data.start_time.minute
            else:
                minute = 0

            hour = int(callback_query.data)
            self.state_manager.data.start_time = time(hour=hour, minute=minute)

            text, reply_markup, state, answer = self.create_minute_message()
        else:
            await callback_query.answer(self.strings.callback_error)
            return

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_minute(self, callback_query: CallbackQuery):
        """Minute menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_hour_message()
        elif callback_query.data.isdigit():
            if self.state_manager.data.start_time:
                hour = self.state_manager.data.start_time.hour
            else:
                hour = 0

            minute = int(callback_query.data)
            self.state_manager.data.start_time = time(hour=hour, minute=minute)

            text, reply_markup, state, answer = self.create_book_message()
        else:
            await callback_query.answer(self.strings.callback_error)
            return

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def callback_list(self, callback_query: CallbackQuery):
        """List menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_main_message()

        elif callback_query.data == "list":
            text, reply_markup, state, answer = self.create_list_message()

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def book_back(self, callback_query: CallbackQuery):
        """Proceed Back button in Book menu"""
        await self.callback_query_action(callback_query,
                                         *self.create_main_message())

    async def book_date(self, callback_query: CallbackQuery):
        """Proceed Date button in Book menu"""
        await self.callback_query_action(callback_query,
                                         *self.create_date_message())

    async def book_time(self, callback_query: CallbackQuery):
        """Proceed Time button in Book menu"""
        await self.callback_query_action(callback_query,
                                         *self.create_hour_message())

    async def book_phone(self, callback_query: CallbackQuery):
        """Proceed Phone button in Book menu"""
        state_manager = self.state_manager
        reserve = self.state_manager.data

        # await callback_query.message.edit_text(self.create_book_text(),
        #                                        reply_markup=None,
        #                                        parse_mode=self.parse_mode)
        await callback_query.message.delete()
        state_manager.finish()

        text, reply_markup, state, answer = self.create_phone_message()

        await self.dispatcher.bot.send_message(callback_query.message.chat.id,
                                               reply_markup=reply_markup,
                                               text=text,
                                               parse_mode=self.parse_mode)
        state_manager.get_state(callback_query.message.chat.id,
                                reserve.user.telegram_id)
        state_manager.set_state(state_type=self.state_type, state=state,
                                data=reserve)

    async def callback_query_action(self,
                                    callback_query: CallbackQuery,
                                    text: str,
                                    reply_markup: InlineKeyboardMarkup,
                                    state: Union[str, int, None],
                                    answer: str):
        """Proceed common CallbackQuery action

        Args:
            callback_query:
                A CallbackQuery instance.
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        state_manager = self.state_manager
        state_manager.set_state(state=state)

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        await callback_query.answer(answer)

    def create_main_message(self):
        """Prepare a main menu message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = self.create_main_text()
        reply_markup = self.create_main_keyboard()
        state = "main"
        answer = self.strings.reserve.main_callback

        return (text, reply_markup, state, answer)

    def create_book_message(self):
        """Prepare a book menu message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = self.create_book_text()
        reply_markup = self.create_book_keyboard()
        state = "book"
        answer = self.strings.reserve.start_book_button_callback

        return (text, reply_markup, state, answer)

    def create_list_message(self):
        """Prepare a list menu message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = self.create_list_text()
        reply_markup = self.create_list_keyboard()
        state = "list"
        answer = self.strings.reserve.list_button_callback

        return (text, reply_markup, state, answer)

    def create_date_message(self):
        """Prepare a date menu message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = self.create_book_text()
        reply_markup = self.create_date_keyboard()
        state = "date"
        answer = self.strings.date_button_callback

        return (text, reply_markup, state, answer)

    def create_hour_message(self):
        """Prepare a hour menu message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = self.create_book_text()
        reply_markup = self.create_hour_keyboard()
        state = "hour"
        answer = self.strings.hour_button_callback

        return (text, reply_markup, state, answer)

    def create_minute_message(self):
        """Prepare a minute menu message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = self.create_book_text()
        reply_markup = self.create_minute_keyboard()
        state = "minute"
        answer = text

        return (text, reply_markup, state, answer)

    def create_phone_message(self):
        """Prepare a phone message

        Returns:
            text:
                A new message text.
            reply_markup:
                A new keyboard reple_markup.
            state:
                A new message state.
            answer:
                A callback answer text.
        """
        text = f"{self.create_book_text()}\n{self.strings.phone_message}"
        reply_markup = ForceReply()
        state = "phone"
        answer = self.strings.phone_button_callback

        return (text, reply_markup, state, answer)

    def create_main_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """

        return "Hello message!"

    def create_book_text(self, show_contact: bool = True) -> str:
        """Create a book menu text

        Returns:
            A message text.
        """

        reserve = self.state_manager.data
        result = ""

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

        result += (f"{self.strings.count_label} "
                   f"{reserve.count}\n")

        return result

    def create_list_text(self) -> str:
        """Create a list menu text

        Returns:
            A message text.
        """
        return "Reserve List menu message text"

    def create_phone_text(self) -> str:
        """Create a phone message text

        Returns:
            A message text.
        """
        return f"{self.create_book_text()}\n{self.strings.phone_message}"

    def create_main_keyboard(self) -> InlineKeyboardMarkup:
        """Create main menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """
        result = InlineKeyboardMarkup(row_width=1)

        button = InlineKeyboardButton(self.strings.reserve.start_book_button,
                                      callback_data='book')
        result.add(button)
        button = InlineKeyboardButton(self.strings.reserve.list_button,
                                      callback_data='list')
        result.add(button)

        return result

    def create_list_keyboard(self) -> InlineKeyboardMarkup:
        """Create list menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """
        result = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

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

        button = InlineKeyboardButton(self.strings.phone_button,
                                      callback_data='phone')
        result.add(button)

        if self.state_manager.data:
            reserve: Reserve = self.state_manager.data
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

    def create_date_keyboard(self) -> InlineKeyboardMarkup:
        """Create Date menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """

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

    def create_hour_keyboard(self, start: int = 9, count: int = 15,
                             row_width: int = 5) -> InlineKeyboardMarkup:
        """Create Hour menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """

        result = InlineKeyboardMarkup(row_width=row_width)

        buttons = [InlineKeyboardButton(f"{start + i}:",
                   callback_data=str(i + self.strings.time_zone))
                   for i in range(count)]

        result.add(*buttons)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_minute_keyboard(self, step: int = 5,
                               row_width: int = 6) -> InlineKeyboardMarkup:
        """Create Hour menu InlineKeyboardMarkup

        Returns:
            A InlineKeyboardMarkup instance.
        """

        result = InlineKeyboardMarkup(row_width=row_width)

        buttons = [InlineKeyboardButton(f"{i}", callback_data=str(i))
                   for i in range(0, 60, step)]

        result.add(*buttons)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    # Temporarry unused
    def create_phone_keyboard(self) -> ReplyKeyboardMarkup:
        """Create Phone message ReplyKeyboardMarkup

        Returns:
            A ReplyKeyboardMarkup instance.
        """
        result = ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
        result.add(KeyboardButton(self.strings.phone_reply_button,
                                  request_contact=True))
        result.add(KeyboardButton(self.strings.phone_refuse_button))
        return result

    def create_reserve(self, message: Message) -> Reserve:
        """Create new Reserve instance
        An update_state method call this when state hasn't an reservation data.

        Returns:
            An Reserve class or child class instance .
        """

        result = Reserve()

        from_user = message.from_user
        user = User(from_user.first_name, from_user.last_name,
                    displayname=from_user.full_name,
                    telegram_id=from_user.id)
        result.user = user

        return result

    def update_state(self, message: Message, message_state: bool = True):
        """Update StateManager for message

        Args:
            message:
                A message to check matching
            message_state:
                A boolean indicates to need use message_id for define state
        """

        super().update_state(message, message_state=message_state)

        if not self.state_manager.data:
            self.state_manager.set_data(self.create_reserve(message))
