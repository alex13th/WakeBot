import sqlite3
from datetime import datetime, date, time, timedelta
from ..mocks.aiogram import Dispatcher
from ..processors.t_reserve import ReserveProcessorTestCase
from .data import users as sup_users

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.sqlite import SqliteSupboardAdapter, SqliteUserAdapter
from wakebot.adapters.state import StateManager
from wakebot.processors import RuSupboard, SupboardProcessor
from wakebot.entities import Supboard


class SupboardProcessorTestCase(ReserveProcessorTestCase):
    "SupboardProcessor class"

    def setUp(self):
        super().setUp()
        self.strings = RuSupboard

        self.dp = Dispatcher()
        self.data_adapter = MemoryDataAdapter()
        self.state_manager = StateManager(self.data_adapter)
        self.processor = SupboardProcessor(self.dp,
                                           self.state_manager, self.strings)
        self.processor.max_count = 6

    def prepare_data(self):
        self.connection = sqlite3.connect("bot_tests/data/sqlite/wake.db")
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS sup_reserves")
        cursor.execute("DROP TABLE IF EXISTS users")
        self.connection.commit()

        self.supboard_adapter = SqliteSupboardAdapter(self.connection)
        self.user_adapter = SqliteUserAdapter(self.connection)

        for user in sup_users:
            self.user_adapter.append_data(user)

        self.reserves = []
        start_time = time(datetime.today().time().hour + 1)
        for i in range(8):
            user = sup_users[i % 5]
            start_date = date.today() + timedelta(i - 2)
            supboard = Supboard(user, start_date=start_date,
                                start_time=start_time,
                                set_count=(i + 1))
            supboard.count = i % 3
            supboard = self.supboard_adapter.append_data(supboard)
            self.reserves.append(supboard)
        self.processor = SupboardProcessor(self.dp, self.state_manager,
                                           self.strings, self.supboard_adapter,
                                           self.user_adapter)
        self.processor.max_count = 6

    def append_state(self, key, state_type="*", state="*"):
        state_data = {}
        state_data["state_type"] = state_type
        state_data["state"] = state
        self.data_adapter.append_data(key, state_data)

    def create_book_keyboard(self):
        """Create book menu InlineKeyboardMarkup"""
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
            reserve: Supboard = self.state_manager.data
            if reserve.is_complete:
                button = InlineKeyboardButton(
                    self.strings.apply_button,
                    callback_data='apply')
                result.add(button)

        # Adding Back-button separately
        button = InlineKeyboardButton(self.strings.back_button,
                                      callback_data='back')
        result.add(button)

        return result

    def create_main_text(self):
        return self.strings.hello_message

    def create_list_text(self):
        if not self.reserves:
            return self.strings.list_empty

        result = f"{self.strings.list_header}\n"
        cur_date = None
        for i in range(2, len(self.reserves)):
            reserve = self.reserves[i]
            if not cur_date or cur_date != reserve.start_date:
                cur_date = reserve.start_date
                result += f"*{cur_date.strftime(self.strings.date_format)}*\n"

            start_time = reserve.start_time.strftime(self.strings.time_format)
            end_time = reserve.end_time.strftime(self.strings.time_format)
            result += f"  {i - 1}. {start_time} - {end_time}"
            result += f" x {reserve.count}"
            result += "\n"

        return result

    def create_book_text(self, show_contact=False):
        reserve = self.state_manager.data
        result = (f"{self.strings.service_label} "
                  f"{self.strings.service_type_text}\n")

        if reserve.user:
            result += f"{self.strings.name_label} {reserve.user.displayname}\n"
            if show_contact and reserve.user.phone_number:
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

        result += f"{self.strings.count_label} {reserve.count}"

        return result

    async def test_cmd_supboard(self):
        """Proceed /sup command"""
        message = self.test_message
        message.text = "/sup"
        reply_markup = self.create_main_keyboard()

        await self.processor.cmd_sup(message)
        state_data = self.data_adapter.get_data_by_keys('101-111-1001')

        passed, message = self.assert_params(
            self.message.text,
            self.strings.hello_message
        )
        assert passed, message

        passed, message = self.assert_params(self.message.reply_markup,
                                             reply_markup)
        assert passed, message

        passed, message = self.assert_params(state_data["state_type"], "sup")
        assert passed, message

        passed, message = self.assert_params(state_data["state"], "main")
        assert passed, message

    async def test_callback_main_book(self):
        """Proceed press Book button in Main menu"""
        callback = self.test_callback_query
        callback.data = "book"
        reply_markup = self.create_book_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "sup", "main")

        checked = self.processor.check_filter(callback.message, "sup", "main")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_main(callback)

        text = self.create_book_text()
        text += f"\n{self.strings.phone_warning}"
        self.check_state(state_key, text,
                         reply_markup, "sup", "book")

    async def test_callback_main_list(self):
        """Proceed press List button in Main menu"""
        self.prepare_data()
        callback = self.test_callback_query
        callback.data = "list"
        reply_markup = self.create_list_keyboard(True)
        state_key = "101-111-121"
        self.append_state(state_key, "sup", "main")

        checked = self.processor.check_filter(
            callback.message, "sup", "main")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        await self.processor.callback_main(callback)

        self.check_state(state_key, self.create_list_text(),
                         reply_markup, "sup", "list")

    async def test_callback_book_date(self):
        """Proceed press Date button in Book menu"""
        callback = self.test_callback_query
        callback.data = "date"
        reply_markup = self.create_date_keyboard()
        state_key = "101-111-121"
        self.append_state(state_key, "sup", "book")

        checked = self.processor.check_filter(callback.message, "sup", "book")
        passed, message = self.assert_params(checked, True)
        assert passed, message

        await self.processor.callback_book(callback)

        self.check_state(state_key, self.create_book_text(),
                         reply_markup, "sup", "date")

    async def test_callback_book_apply(self):
        """Proceed Apply button in Book menu"""
        self.prepare_data()
        callback = self.test_callback_query
        callback.data = "apply"
        state_key = "101-111-121"
        self.append_state(state_key, "sup", "book")

        checked = self.processor.check_filter(
            callback.message, "sup", "book")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert

        self.reserves[2].start_time = time(22)
        self.state_manager.set_state(data=self.reserves[2])
        await self.processor.callback_book(callback)

        reserve = self.state_manager.data
        reserve = self.supboard_adapter.get_data_by_keys(reserve.id)

        passed, alert = self.assert_params(reserve.set_count, 3)
        assert passed, alert

        # Check that state is finished
        state_data = self.data_adapter.get_data_by_keys(state_key)
        passed, alert = self.assert_params(state_data, None)
        assert passed, alert

    async def test_callback_details_cancel(self):
        """Proceed press Cancel button in Details menu"""
        self.prepare_data()

        callback = self.test_callback_query

        callback.data = "cancel-4"
        state_key = "101-111-121"
        self.append_state(state_key, "sup", "details")

        checked = self.processor.check_filter(
            callback.message, "sup", "details")
        passed, alert = self.assert_params(checked, True)
        assert passed, alert
        reserve = self.supboard_adapter.get_data_by_keys(4)

        await self.processor.callback_details(callback)

        del self.reserves[3]
        reserve = self.supboard_adapter.get_data_by_keys(4)

        passed, alert = self.assert_params(reserve.canceled, True)
        assert passed, alert

        text = self.create_list_text()
        reply_markup = self.create_list_keyboard(True)
        self.check_state(state_key, text,
                         reply_markup, "sup", "list")


if __name__ == "__main__":
    SupboardProcessorTestCase().run_tests_async()
