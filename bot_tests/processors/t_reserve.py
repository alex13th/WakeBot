from ..base_test_case import BaseTestCase
from ..mocks.aiogram import Dispatcher

from datetime import date, time, timedelta

from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager
from wakebot.processors import RuGeneral, ReserveProcessor
from wakebot.entities import Reserve

from aiogram.types import Message, CallbackQuery, Chat, User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ReserveProcessorTestCase(BaseTestCase):
    "ReserveProcessor class"

    def setUp(self):
        self.reserves = []
        self.strings = RuGeneral

        self.chat = Chat()
        self.chat.id = 101
        self.user = User()
        self.user.first_name = "Firstname"
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
        message.delete = self.delete_mock
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
        answer = Message()
        answer.message_id = 1001
        answer.from_user = self.user
        answer.chat = self.chat
        return answer

    async def delete_mock(self):
        pass

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

    def create_book_text(self, show_contact=False):
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

    def create_list_text(self):
        if not self.reserves:
            return self.strings.reserve.list_empty

        result = f"{self.strings.reserve.list_header}\n"
        cur_date = None
        for i in range(2, 8):
            reserve = self.reserves[i]
            if not cur_date or cur_date != reserve.start_date:
                cur_date = reserve.start_date
                result += f"*{cur_date.strftime(self.strings.date_format)}*\n"

            start_time = reserve.start_time.strftime(self.strings.time_format)
            end_time = reserve.end_time.strftime(self.strings.time_format)
            result += f"  {i - 1}. {start_time} - {end_time}"
            result += (f" {self.strings.wake.icon_board}x{reserve.board}"
                       if reserve.board else "")
            result += (f" {self.strings.wake.icon_hydro}x{reserve.hydro}"
                       if reserve.hydro else "")
            result += "\n"

        return f"{result}\n{self.strings.reserve.list_footer}"

    def create_phone_text(self):
        return f"{self.create_book_text()}\n{self.strings.phone_message}"

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
        """Create book menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=1)

        button = InlineKeyboardButton(self.strings.reserve.count_button,
                                      callback_data='count')
        result.add(button)

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

    def create_list_keyboard(self):
        """Create List menu InlineKeyboardMarkup"""
        result = InlineKeyboardMarkup(row_width=5)
        count = len(self.reserves) if self.reserves else 0
        buttons = []
        for i in range(count - 2):
            buttons.append(InlineKeyboardButton(
                str(i + 1), callback_data=str(self.reserves[i + 2].id)))

        result.add(*buttons)

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

        buttons = [InlineKeyboardButton(f"{start + i}:",
                   callback_data=str(i + self.strings.time_zone))
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

    def create_count_keyboard(self, count: int, start: int = 1,
                              row_width: int = 6):
        """Create Hour menu InlineKeyboardMarkup"""

        result = InlineKeyboardMarkup(row_width=row_width)

        buttons = [InlineKeyboardButton(f"{i}", callback_data=str(i))
                   for i in range(start, count + 1)]

        result.add(*buttons)
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_details_keyboard(self,
                                reserve: Reserve) -> InlineKeyboardMarkup:

        result = InlineKeyboardMarkup(row_width=1)
        buttons = []
        buttons.append(InlineKeyboardButton(
            self.strings.reserve.cancel_button,
            callback_data=f"cancel-{reserve.id}"))

        buttons.append(InlineKeyboardButton(
            self.strings.reserve.notify_button,
            callback_data=f"notify-{reserve.id}"))

        buttons.append(InlineKeyboardButton(
            self.strings.back_button,
            callback_data="back"))

        result.add(*buttons)

        return result

    async def test_callback_main_book(self):
        """Proceed press Book button in Main menu"""
        callback = self.test_callback_query
        callback.data = "book"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "main")

        checked = self.processor.check_filter(
            callback.message, "reserve", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_main(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_book_back(self):
        """Proceed press Back button in Book menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_main_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(
            callback.message, "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_main_text(),
                         reply_markup, "reserve", "main")

    async def test_callback_book_date(self):
        """Proceed press Date button in Book menu"""
        callback = self.test_callback_query
        callback.data = "date"
        reply_markup = self.create_date_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(
            callback.message, "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "date")

    async def test_callback_date_back(self):
        """Proceed press Back button in Date menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "date")

        checked = self.processor.check_filter(
            callback.message, "reserve", "date")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_date(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_date_date(self):
        """Proceed select date in Date menu"""
        callback = self.test_callback_query
        callback.data = "1"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "date")

        checked = self.processor.check_filter(
            callback.message, "reserve", "date")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_date(callback)

        reserve = self.state_manager.data
        passed, alert = self.assert_params(date.today() + timedelta(1),
                                           reserve.start_date)
        assert passed, alert
        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_book_time(self):
        """Proceed press Time button in Book menu"""
        callback = self.test_callback_query
        callback.data = "time"
        reply_markup = self.create_hour_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(callback.message,
                                              "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "hour")

    async def test_callback_book_phone(self):
        """Proceed press Phone button in Book menu"""
        callback = self.test_callback_query
        callback.data = "phone"
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "book")

        checked = self.processor.check_filter(
            callback.message, "reserve", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_book(callback)

        text = self.create_phone_text()
        state_key = "101-111"
        state_data = self.data_adapter.get_data_by_keys(state_key)
        passed, alert = self.assert_params(state_data["state_type"],
                                           self.processor.state_type)
        assert passed, alert
        passed, alert = self.assert_params(state_data["state"],
                                           "phone")
        assert passed, alert

        passed, alert = self.assert_params(self.processor.dispatcher.bot.text,
                                           text)
        assert passed, alert

    async def test_callback_hour_back(self):
        """Proceed press Back button in Hour menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "hour")

        checked = self.processor.check_filter(
            callback.message, "reserve", "hour")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_hour(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_minute(self):
        """Proceed select hour in Hour menu"""
        callback = self.test_callback_query
        callback.data = "18"
        reply_markup = self.create_minute_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "hour")

        checked = self.processor.check_filter(
            callback.message, "reserve", "hour")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_hour(callback)

        reserve = self.state_manager.data
        passed, alert = self.assert_params(time(hour=18),
                                           reserve.start_time)
        assert passed, alert

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "minute")

    async def test_callback_minute_back(self):
        """Proceed press Back button in Minute menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_hour_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "minute")

        checked = self.processor.check_filter(
            callback.message, "reserve", "minute")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_minute(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "hour")

    async def test_callback_minute_minute(self):
        """Proceed select minute in Minute menu"""
        callback = self.test_callback_query
        callback.data = "30"
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "minute")

        checked = self.processor.check_filter(
            callback.message, "reserve", "minute")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        reserve = self.state_manager.data
        reserve.start_time = time(16, 15)

        await self.processor.callback_minute(callback)

        passed, alert = self.assert_params(time(hour=16, minute=30),
                                           reserve.start_time)
        assert passed, alert

        reply_markup = self.create_book_keyboard()
        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_book_set(self):
        """Proceed press Set button in Book menu"""
        callback = self.test_callback_query
        callback.data = "set"
        reply_markup = self.create_count_keyboard(6)
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "book")

        checked = self.processor.check_filter(callback.message, "wake", "book")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "set")

    async def test_callback_set_back(self):
        """Proceed press Back button in Set menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "set")

        checked = self.processor.check_filter(
            callback.message, "reserve", "set")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_set(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_set_count(self):
        """Proceed select Count in Set menu"""
        callback = self.test_callback_query
        callback.data = "3"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "set")

        checked = self.processor.check_filter(
            callback.message, "reserve", "set")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_set(callback)

        reserve = self.state_manager.data

        passed, alert = self.assert_params(3, reserve.set_count)
        assert passed, alert

        passed, alert = self.assert_params("set", reserve.set_type.set_id)
        assert passed, alert

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_book_set_hour(self):
        """Proceed press Set Hour button in Book menu"""
        callback = self.test_callback_query
        callback.data = "set_hour"
        reply_markup = self.create_count_keyboard(6)
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "book")

        checked = self.processor.check_filter(callback.message, "wake", "book")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "set_hour")

    async def test_callback_set_hour_back(self):
        """Proceed press Back button in Set Hour menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "set_hour")

        checked = self.processor.check_filter(
            callback.message, "reserve", "set_hour")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_set_hour(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_set_hour_count(self):
        """Proceed select Count in Set Hour menu"""
        callback = self.test_callback_query
        callback.data = "2"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "set_hour")

        checked = self.processor.check_filter(
            callback.message, "reserve", "set_hour")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_set_hour(callback)

        reserve = self.state_manager.data

        passed, alert = self.assert_params(2, reserve.set_count)
        assert passed, alert

        passed, alert = self.assert_params("hour", reserve.set_type.set_id)
        assert passed, alert

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "reserve", "book")

    async def test_callback_main_list(self):
        """Proceed press List button in Main menu"""
        callback = self.test_callback_query
        callback.data = "list"
        reply_markup = self.create_list_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "main")

        checked = self.processor.check_filter(
            callback.message, "reserve", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_main(callback)

        self.check_state(state_key, self.create_list_text(),
                         reply_markup, "reserve", "list")

    async def test_callback_list_back(self):
        """Proceed press Back button in List menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_main_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "reserve", "list")

        checked = self.processor.check_filter(
            callback.message, "reserve", "list")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_list(callback)

        self.check_state(state_key, self.create_main_text(),
                         reply_markup, "reserve", "main")

    def check_state(self, key, text, reply_markup,
                    state_type=None, state=None, data=None):
        """A util method to check current state"""

        state_data = self.data_adapter.get_data_by_keys(key)

        passed, alert = self.assert_params(self.message.text, text)
        assert passed, alert
        passed, alert = self.assert_params(self.message.reply_markup,
                                           reply_markup)
        assert passed, alert
        passed, alert = self.assert_params(state_data["state"], state)
        assert passed, alert
        if state_type:
            passed, alert = self.assert_params(state_data["state_type"],
                                               state_type)
            assert passed, alert
        if data:
            passed, alert = self.assert_params(state_data["data"], data)
            assert passed, alert


if __name__ == "__main__":
    ReserveProcessorTestCase().run_tests_async()
