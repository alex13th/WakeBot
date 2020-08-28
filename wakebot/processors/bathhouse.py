from typing import Union
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import ChatNotFound, BotBlocked

from ..adapters.state import StateManager
from .reserve import ReserveProcessor
from ..entities import User, Bathhouse, ReserveSetType, Reserve
from ..adapters.data import ReserveDataAdapter, UserDataAdapter


class BathhouseProcessor(ReserveProcessor):
    """Proceed a Bathhouse reservaion process

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
                 state_type: Union[str, int, None] = "bathhouse"):
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
                Default value: "bathhouse"
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        super().__init__(dispatcher, state_manager, strings,
                         data_adapter=data_adapter,
                         user_data_adapter=user_data_adapter,
                         state_type=state_type)

        self.minute_step = 10
        self.reserve_set_types["hour"] = ReserveSetType("hour", 60)

        dispatcher.register_message_handler(self.cmd_booking,
                                            commands=["booking"])

        self.book_handlers["apply"] = self.book_apply

    async def cmd_booking(self, message: Message):
        """Proceed /booking command"""

        from_user = message.from_user
        user = None
        if self.user_data_adapter:
            user = self.user_data_adapter.get_user_by_telegram_id(from_user.id)
            self.admin_telegram_ids = [user.telegram_id
                                       for user
                                       in self.user_data_adapter.get_admins()]
            text, reply_markup, state, _ = self.create_main_message(
                user.is_admin)
        else:
            text, reply_markup, state, _ = self.create_main_message()

        answer = await message.answer(
            text,
            reply_markup=reply_markup,
            parse_mode=self.parse_mode)

        self.update_state(answer, message_state=True)
        state_manager = self.state_manager

        reserve = self.create_reserve(answer)

        if not user:
            user = User(from_user.first_name, from_user.last_name,
                        displayname=from_user.full_name,
                        telegram_id=from_user.id)
            # if self.user_data_adapter:
            #     user = self.user_data_adapter.append_data(user)

        reserve.user = user

        state_manager.set_state(
            state_type=self.state_type, state="main", data=reserve)

    def create_main_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """
        reserve_list = None
        if self.data_adapter:
            reserve_list = list(self.data_adapter.get_active_reserves())

        return self.create_list_text(reserve_list)

    def create_book_text(self,
                         reserve: Bathhouse,
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
        result: str = ""

        if reserve.start_time:
            start_time = reserve.start_time.strftime(self.strings.time_format)
            result += (f"{self.strings.start_label} "
                       f"{start_time}\n")
            end_time = reserve.end_time.strftime(self.strings.time_format)
            result += (f"{self.strings.end_label} "
                       f"{end_time}\n")

        return result

    def create_reserve_text(self, reserve: Bathhouse) -> str:
        result = ""
        start_time = reserve.start_time.strftime(self.strings.time_format)
        end_time = reserve.end_time.strftime(self.strings.time_format)
        result += f"{start_time} - {end_time}"

        return result

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
        reserve: Reserve = self.state_manager.data
        text = self.strings.booking_text

        conflicted = False
        if self.data_adapter:
            conflicted, concurrent_text = self.check_concurrents(reserve)
            if conflicted:
                text = self.strings.concurrent_text

        ready = reserve.is_complete and not conflicted
        reply_markup = self.create_book_keyboard(ready)

        answer = self.strings.start_book_button_callback
        state = "book"

        return (text, reply_markup, state, answer)

    def create_book_keyboard(self, ready=False) -> InlineKeyboardMarkup:
        """Create book menu InlineKeyboardMarkup
        Args:
            ready:
                Ready to apply reservation flag.
        Returns:
            A InlineKeyboardMarkup instance.
        """
        result = InlineKeyboardMarkup(row_width=6)

        if self.state_manager.data:
            if ready:
                button = InlineKeyboardButton(
                    self.strings.apply_button,
                    callback_data='apply')
                result.add(button)
                button = InlineKeyboardButton(self.strings.time_button_change,
                                              callback_data='time')
            else:
                button = InlineKeyboardButton(self.strings.time_button,
                                              callback_data='time')

        result.add(button)

        return result

    async def cancel_reserve(self,
                             callback_query: CallbackQuery,
                             reserve_id: int):
        """Cancel reservation

        Args:
            callback_query:
                A CallbackQuery instance.
            reserve_id:
                An integer reservation identifier.
        """
        telegram_id = callback_query.from_user.id
        reserve = self.data_adapter.get_data_by_keys(reserve_id)
        reserve.canceled = True
        reserve.cancel_telegram_id = telegram_id
        self.data_adapter.update_data(reserve)

        notify_text = self.strings.cancel_notify_header
        notify_text += f"\n\n{self.create_reserve_text(reserve)}"

        for telegram_id in self.admin_telegram_ids:
            if not telegram_id == callback_query.from_user.id:
                try:
                    await callback_query.bot.send_message(
                        telegram_id, notify_text,
                        reply_markup=None,
                        parse_mode=self.parse_mode)
                except ChatNotFound:
                    await self.send_to_logger(f"ChatNotFound: {telegram_id}")
                except BotBlocked:
                    await self.send_to_logger(f"BotBlocked: {telegram_id}")
        await callback_query.bot.send_message(
            reserve.user.telegram_id, notify_text,
            reply_markup=None,
            parse_mode=self.parse_mode)

    def create_reserve(self, message: Message) -> Bathhouse:
        """Create new Reserve instance
        An update_state method call this when state hasn't an reservation data.

        Returns:
            An Wake class or child class instance .
        """
        result = Bathhouse()

        from_user = message.from_user
        user = User(from_user.first_name, from_user.last_name,
                    displayname=from_user.full_name, telegram_id=from_user.id)
        result.user = user

        return result

    async def callback_details(self, callback_query: CallbackQuery):
        """Detail menu CallbackQuery handler"""
        # State manager updated by StatedProcessor check_filter method

        text = reply_markup = state = None

        if callback_query.data == "back":
            text, reply_markup, state, answer = self.create_list_message(True)

        elif callback_query.data.startswith("cancel-"):
            reserve_id = int(callback_query.data[7:])
            await self.cancel_reserve(callback_query, reserve_id)
            text, reply_markup, state, answer = self.create_list_message(True)
            answer = self.strings.cancel_button_callback

        elif callback_query.data.startswith("notify-"):
            reserve_id = int(callback_query.data[7:])
            reserve = self.data_adapter.get_data_by_keys(reserve_id)

            notify_text = self.strings.notify_message
            await callback_query.bot.send_message(reserve.user.telegram_id,
                                                  notify_text,
                                                  parse_mode=self.parse_mode)

            text, reply_markup, state, answer = self.create_list_message(True)
            answer = self.strings.notify_button_callback

        await callback_query.message.edit_text(text,
                                               reply_markup=reply_markup,
                                               parse_mode=self.parse_mode)
        self.state_manager.set_state(state=state)
        await callback_query.answer(answer)

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
        reserve_list = None
        if self.data_adapter:
            reserve_list = list(self.data_adapter.get_active_reserves())

        text = self.create_list_text(reserve_list)
        text += f"\n{self.strings.hour_notes}"
        reply_markup = self.create_hour_keyboard(start=9, count=20)
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
        reserve_list = None
        if self.data_adapter:
            reserve_list = list(self.data_adapter.get_active_reserves())

        text = self.create_list_text(reserve_list)
        text += f"\n{self.strings.minute_notes}"
        reply_markup = self.create_minute_keyboard(step=self.minute_step)
        state = "minute"
        answer = self.strings.minute_button_callback

        return (text, reply_markup, state, answer)

    def create_detail_message(self, reserve_id: int):
        reserve: Reserve = self.data_adapter.get_data_by_keys(reserve_id)
        text: str = ""

        if reserve.user:
            text += f"{self.strings.name_label} {reserve.user.displayname}\n"

        text += self.create_book_text(reserve, show_contact=True)
        reply_markup = self.create_details_keyboard(reserve)
        state = "details"
        answer = self.strings.cancel_button_callback

        return (text, reply_markup, state, answer)
