import sqlite3
from datetime import datetime, date, time, timedelta
from ..mocks.aiogram import Dispatcher
from ..processors.t_reserve import ReserveProcessorTestCase
from .data import users as wake_users

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.sqlite import SqliteWakeAdapter, SqliteUserAdapter
from wakebot.adapters.state import StateManager
from wakebot.processors import RuGeneral, WakeProcessor
from wakebot.entities import Wake


class WakeProcessorTestCase(ReserveProcessorTestCase):
    "WakeProcessor class"

    def setUp(self):
        super().setUp()
        self.strings = RuGeneral

        self.dp = Dispatcher()
        self.data_adapter = MemoryDataAdapter()
        self.state_manager = StateManager(self.data_adapter)
        self.processor = WakeProcessor(self.dp, self.state_manager,
                                       self.strings)

    def prepare_data(self):
        self.connection = sqlite3.connect("bot_tests/data/sqlite/wake.db")
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS wake_reserves")
        cursor.execute("DROP TABLE IF EXISTS users")
        self.connection.commit()

        self.wake_adapter = SqliteWakeAdapter(self.connection)
        self.user_adapter = SqliteUserAdapter(self.connection)

        for user in wake_users:
            self.user_adapter.append_data(user)

        self.reserves = []
        start_time = time(datetime.today().time().hour + 1)
        for i in range(8):
            user = wake_users[i % 5]
            start_date = date.today() + timedelta(i - 2)
            wake = Wake(user, start_date=start_date, start_time=start_time,
                        set_count=(i + 1))
            wake.board = i % 2
            wake.hydro = i % 3
            wake = self.wake_adapter.append_data(wake)
            self.reserves.append(wake)
        self.processor = WakeProcessor(self.dp, self.state_manager,
                                       self.strings,
                                       self.wake_adapter, self.user_adapter)

    def append_state(self, key, state_type="*", state="*"):
        state_data = {}
        state_data["state_type"] = state_type
        state_data["state"] = state
        self.data_adapter.append_data(key, state_data)

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

    def create_main_text(self):
        return self.strings.wake.hello_message

    def create_list_text(self):
        if not self.reserves:
            return self.strings.reserve.list_empty

        result = f"{self.strings.reserve.list_header}\n"
        cur_date = None
        for i in range(2, len(self.reserves)):
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

        return result

    def create_book_text(self, show_contact=False):
        reserve = self.state_manager.data
        result = (f"{self.strings.reserve.type_label} "
                  f"{RuGeneral.wake.wake_text}\n")

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

    async def test_cmd_wake(self):
        """Proceed /wake command"""
        message = self.test_message
        message.text = "/wake"
        reply_markup = self.create_main_keyboard()

        await self.processor.cmd_wake(message)
        state_data = self.data_adapter.get_data_by_keys('101-111-1001')

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

        checked = self.processor.check_filter(callback.message, "wake", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_main(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "book")

    async def test_callback_main_list(self):
        """Proceed press List button in Main menu"""
        self.prepare_data()
        callback = self.test_callback_query
        callback.data = "list"
        reply_markup = self.create_list_keyboard(True)
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "main")

        checked = self.processor.check_filter(
            callback.message, "wake", "main")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_main(callback)

        self.check_state(state_key, self.create_list_text(),
                         reply_markup, "wake", "list")

    async def test_callback_book_date(self):
        """Proceed press Date button in Book menu"""
        callback = self.test_callback_query
        callback.data = "date"
        reply_markup = self.create_date_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "book")

        checked = self.processor.check_filter(callback.message, "wake", "book")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "date")

    async def test_callback_book_board(self):
        """Proceed press Board button in Book menu"""
        callback = self.test_callback_query
        callback.data = "board"
        reply_markup = self.create_count_keyboard(start=0, count=3)
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "book")

        checked = self.processor.check_filter(
            callback.message, "wake", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "board")

    async def test_callback_board_back(self):
        """Proceed press Back button in Board menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "board")

        checked = self.processor.check_filter(
            callback.message, "wake", "board")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_board(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "book")

    async def test_callback_board_count(self):
        """Proceed select Count in Board menu"""
        callback = self.test_callback_query
        callback.data = "2"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "board")

        checked = self.processor.check_filter(
            callback.message, "wake", "board")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_board(callback)

        reserve = self.state_manager.data

        passed, alert = self.assert_params(2, reserve.board)
        assert passed, alert

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "book")

    async def test_callback_book_hydro(self):
        """Proceed press Hydro button in Book menu"""
        callback = self.test_callback_query
        callback.data = "hydro"
        reply_markup = self.create_count_keyboard(start=0, count=3)
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "book")

        checked = self.processor.check_filter(
            callback.message, "wake", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "hydro")

    async def test_callback_hydro_back(self):
        """Proceed press Back button in Hydro menu"""
        callback = self.test_callback_query
        callback.data = "back"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "hydro")

        checked = self.processor.check_filter(
            callback.message, "wake", "hydro")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_hydro(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "book")

    async def test_callback_hydro_count(self):
        """Proceed select Count in Hydro menu"""
        callback = self.test_callback_query
        callback.data = "3"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "hydro")

        checked = self.processor.check_filter(
            callback.message, "wake", "hydro")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_hydro(callback)

        reserve = self.state_manager.data

        passed, alert = self.assert_params(3, reserve.hydro)
        assert passed, alert

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "wake", "book")

    async def test_callback_book_apply(self):
        """Proceed Apply button in Book menu"""
        self.prepare_data()
        callback = self.test_callback_query
        callback.data = "apply"
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "book")

        checked = self.processor.check_filter(
            callback.message, "wake", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        self.reserves[2].start_time = time(4)
        self.state_manager.set_state(data=self.reserves[2])
        await self.processor.callback_book(callback)

        reserve = self.state_manager.data
        reserve = self.wake_adapter.get_data_by_keys(reserve.id)

        passed, alert = self.assert_params(reserve.set_count, 3)
        assert passed, alert

        # Check that state is finished
        state_data = self.data_adapter.get_data_by_keys(state_key)
        passed, alert = self.assert_params(state_data, None)
        assert passed, alert

    async def test_callback_list_details(self):
        """Proceed press Details button in List menu"""
        self.prepare_data()

        callback = self.test_callback_query
        callback.data = "4"
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "list")

        checked = self.processor.check_filter(
            callback.message, "wake", "list")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_list(callback)

        self.state_manager.set_state(data=self.reserves[3])
        reply_markup = self.create_details_keyboard(reserve=self.reserves[3])
        self.check_state(state_key, self.create_book_text(True),
                         reply_markup, "wake", "details")

    async def test_callback_details_cancel(self):
        """Proceed press Cancel button in Details menu"""
        self.prepare_data()

        callback = self.test_callback_query

        callback.data = "cancel-4"
        state_key = "101-111-121"
        self.append_state(state_key, "wake", "details")

        checked = self.processor.check_filter(
            callback.message, "wake", "details")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert
        reserve = self.wake_adapter.get_data_by_keys(4)

        await self.processor.callback_details(callback)

        del self.reserves[3]
        reserve = self.wake_adapter.get_data_by_keys(4)

        passed, alert = self.assert_params(reserve, None)
        assert passed, alert

        text = self.create_list_text()
        reply_markup = self.create_list_keyboard(True)
        self.check_state(state_key, text,
                         reply_markup, "wake", "list")


if __name__ == "__main__":
    WakeProcessorTestCase().run_tests_async()
