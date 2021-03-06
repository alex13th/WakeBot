from typing import Union
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher

from ..adapters.state import StateManager
from .reserve import ReserveProcessor
from ..entities import User, Supboard, ReserveSetType
from ..adapters.data import ReserveDataAdapter, UserDataAdapter


class SupboardProcessor(ReserveProcessor):
    """Proceed a supboard reservaion process

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
                 state_type: Union[str, int, None] = "sup"):
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
                Default value: "sup"
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        super().__init__(dispatcher, state_manager, strings,
                         data_adapter=data_adapter,
                         user_data_adapter=user_data_adapter,
                         state_type=state_type)

        self.reserve_set_types["set"] = ReserveSetType("set", 30)

        dispatcher.register_message_handler(self.cmd_sup, commands=["sup"])

        self.book_handlers["apply"] = self.book_apply

    async def cmd_sup(self, message: Message):
        """Proceed /sup command"""

        text, reply_markup, state, _ = self.create_main_message()

        answer = await message.answer(
            self.strings.hello_message,
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
            # if self.user_data_adapter:
            #     user = self.user_data_adapter.append_data(user)

        reserve.user = user

        state_manager.set_state(state_type="sup", state="main", data=reserve)

    def create_main_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """

        return self.strings.hello_message

    def create_book_text(self,
                         reserve: Supboard,
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

        result = (f"{self.strings.service_label} "
                  f"{self.strings.service_type_text}\n")

        if reserve.user and show_contact:
            result += f"{self.strings.name_label} {reserve.user.displayname}\n"
            if reserve.user.phone_number:
                result += (f"{self.strings.phone_label} "
                           f"{reserve.user.phone_number}\n")

        result += (f"{self.strings.date_label} "
                   f"{reserve.start_date.strftime(self.strings.date_format)}"
                   "\n")

        if reserve.start_time:
            start_time = reserve.start_time.strftime(self.strings.time_format)
            result += (f"{self.strings.start_label} "
                       f"{start_time}\n")
            end_time = reserve.end_time.strftime(self.strings.time_format)
            result += (f"{self.strings.end_label} "
                       f"{end_time}\n")

        result += (f"{self.strings.set_type_label} "
                   f"{self.strings.set_types[reserve.set_type.set_id]}"
                   f" ({reserve.set_count})\n")

        result += (f"{self.strings.count_label}"
                   f" {reserve.count}")

        return result

    def create_reserve_text(self, reserve: Supboard) -> str:
        result = ""
        start_time = reserve.start_time.strftime(self.strings.time_format)
        end_time = reserve.end_time.strftime(self.strings.time_format)
        result += f"{start_time} - {end_time}"
        result += f" x {reserve.count}"

        return result

    def create_book_keyboard(self, ready=False) -> InlineKeyboardMarkup:
        """Create book menu InlineKeyboardMarkup
        Args:
            ready:
                Ready to apply reservation flag.
        Returns:
            A InlineKeyboardMarkup instance.
        """
        result = InlineKeyboardMarkup(row_width=6)

        button = InlineKeyboardButton(self.strings.count_button,
                                      callback_data='count')
        result.add(button)

        # Adding Date- and Time- buttons by a row for each
        button = InlineKeyboardButton(self.strings.date_button,
                                      callback_data='date')
        result.add(button)
        button = InlineKeyboardButton(self.strings.time_button,
                                      callback_data='time')
        result.add(button)

        # Adding Set- and Hour- buttons in one row
        set_button = InlineKeyboardButton(self.strings.set_button,
                                          callback_data='set')
        hour_button = InlineKeyboardButton(self.strings.hour_button,
                                           callback_data='set_hour')
        result.row(set_button, hour_button)

        button = InlineKeyboardButton(self.strings.phone_button,
                                      callback_data='phone')
        result.add(button)

        if self.state_manager.data:
            if ready:
                button = InlineKeyboardButton(
                    self.strings.apply_button,
                    callback_data='apply')
                result.add(button)

        # Adding Back-button separately
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_reserve(self, message: Message) -> Supboard:
        """Create new Reserve instance
        An update_state method call this when state hasn't an reservation data.

        Returns:
            An Wake class or child class instance .
        """
        result = Supboard()

        from_user = message.from_user
        user = User(from_user.first_name, from_user.last_name,
                    displayname=from_user.full_name, telegram_id=from_user.id)
        result.user = user

        return result
