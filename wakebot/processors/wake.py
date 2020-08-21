from typing import Union
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher

from ..adapters.state import StateManager
from .reserve import ReserveProcessor
from ..entities import User, Wake, ReserveSetType
from ..adapters.data import ReserveDataAdapter, UserDataAdapter


class WakeProcessor(ReserveProcessor):
    """Proceed a wake reservaion process

    Attributes:
        dispatcher:
            A telegram bot dispatcher instance instance.
        state_manager:
            A state manager class instance
        strings:
            A locale strings class
        data_adapter:
            A reservation storage data adapter
        user_data_adapter:
            An user storage data adapter
        book_handlers:
            A dictionary of book menu handlers.
            A key matches InlineKeyboardButton.data value of book menu.
            A value must contain handler function - f().
    """

    def __init__(self,
                 dispatcher: Dispatcher,
                 state_manager: StateManager,
                 strings: any,
                 data_adapter: Union[ReserveDataAdapter, None] = None,
                 user_data_adapter: Union[UserDataAdapter, None] = None,
                 state_type: Union[str, int, None] = "wake"):
        """Initialize a class instance

        Args:
            dispatcher:
                A telegram bot dispatcher instance instance.
            state_manager:
                A state manager class instance
            strings:
                A locale strings class.
            data_adapter:
                Optional. A reservation storage data adapter
            user_data_adapter:
                Optional. An user storage data adapter
            state_type:
                Optional, A default state type.
                Default value: "wake"
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        super().__init__(dispatcher, state_manager, strings,
                         data_adapter=data_adapter,
                         user_data_adapter=user_data_adapter,
                         state_type=state_type)

        self.reserve_set_types["set"] = ReserveSetType("set", 10)

        dispatcher.register_message_handler(self.cmd_wake, commands=["wake"])

        self.register_callback_query_handler(self.callback_board, "board")
        self.register_callback_query_handler(self.callback_hydro, "hydro")

        self.book_handlers["board"] = self.book_board
        self.book_handlers["hydro"] = self.book_hydro

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

        user = None
        if self.user_data_adapter:
            user = self.user_data_adapter.get_user_by_telegram_id(from_user.id)
            self.admin_telegram_ids = [user.telegram_id
                                       for user
                                       in self.user_data_adapter.get_admins()]

        if not user:
            user = User(from_user.first_name, from_user.last_name,
                        displayname=from_user.full_name,
                        telegram_id=from_user.id)
            if self.user_data_adapter:
                user = self.user_data_adapter.append_data(user)

        reserve.user = user

        state_manager.set_state(state_type="wake", state="main", data=reserve)

    async def callback_board(self, callback_query: CallbackQuery):
        """Board menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_book_message()
        elif callback_query.data.isdigit():
            self.state_manager.data.board = int(callback_query.data)
            text, reply_markup, state, answer = self.create_book_message()
        else:
            await callback_query.answer(self.strings.callback_error)
            return

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def book_board(self, callback_query: CallbackQuery):
        """Proceed Board button in Book menu"""
        await self.callback_query_action(callback_query,
                                         *self.create_board_message())

    def create_board_message(self):
        """Prepare a Board menu message

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
        reserve: Wake = self.state_manager.data
        text = self.create_book_text(reserve, show_contact=True)
        reply_markup = self.create_count_keyboard(start=0, count=3)
        state = "board"
        answer = self.strings.wake.board_button_callback

        return (text, reply_markup, state, answer)

    async def callback_hydro(self, callback_query: CallbackQuery):
        """Hydro menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None
        state_manager = self.state_manager

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_book_message()
        elif callback_query.data.isdigit():
            self.state_manager.data.hydro = int(callback_query.data)
            text, reply_markup, state, answer = self.create_book_message()
        else:
            await callback_query.answer(self.strings.callback_error)
            return

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        state_manager.set_state(state=state)
        await callback_query.answer(answer)

    async def book_hydro(self, callback_query: CallbackQuery):
        """Proceed Board button in Book menu"""
        await self.callback_query_action(callback_query,
                                         *self.create_hydro_message())

    def create_hydro_message(self):
        """Prepare a Board menu message

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
        reserve: Wake = self.state_manager.data
        text = self.create_book_text(reserve, show_contact=True)
        reply_markup = self.create_count_keyboard(start=0, count=3)
        state = "hydro"
        answer = self.strings.wake.hydro_button_callback

        return (text, reply_markup, state, answer)

    def create_main_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """

        return self.strings.wake.hello_message

    def create_book_text(self,
                         reserve: Wake,
                         check=True,
                         show_contact: bool = False) -> str:
        """Create a book menu text
        Args:
            check:
                Optional. A boolean value means to need check
                concurrent reservations.
            show_contact:
                Optional. A boolean value means to allow
                show contact information

        Returns:
            A message text.
        """

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

        if reserve.board or reserve.hydro:
            result += self.strings.wake.options_label
            result += (f" {self.strings.wake.icon_board}x{reserve.board}"
                       if reserve.board else "")
            result += (f" {self.strings.wake.icon_hydro}x{reserve.hydro}"
                       if reserve.hydro else "")

        return result

    def create_reserve_text(self, reserve: Wake) -> str:
        result = ""
        start_time = reserve.start_time.strftime(self.strings.time_format)
        end_time = reserve.end_time.strftime(self.strings.time_format)
        result += f"{start_time} - {end_time}"
        result += (f" {self.strings.wake.icon_board}x{reserve.board}"
                   if reserve.board else "")
        result += (f" {self.strings.wake.icon_hydro}x{reserve.hydro}"
                   if reserve.hydro else "")

        return result

    def create_book_keyboard(self, ready=False) -> InlineKeyboardMarkup:
        """Create book menu InlineKeyboardMarkup
        Args:
            ready:
                Ready to apply reservation flag.
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
                                          callback_data='board')
        hour_button = InlineKeyboardButton(self.strings.wake.hydro_button,
                                           callback_data='hydro')
        result.row(set_button, hour_button)

        button = InlineKeyboardButton(self.strings.phone_button,
                                      callback_data='phone')
        result.add(button)

        if self.state_manager.data:
            if ready:
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
