import sqlite3
from datetime import datetime, date, time, timedelta
from ...base_test_case import BaseTestCase
from wakebot.adapters.sqlite import SqliteSupboardAdapter
from wakebot.entities import Supboard, User


class SqliteSupboardAdapterTestCase(BaseTestCase):
    """SqliteSupboardAdapter class"""
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("bot_tests/data/sqlite/wake.db")

    def setUp(self):
        self.drop_table()
        self.adapter = SqliteSupboardAdapter(self.connection)
        self.user = User("Firstname", telegram_id=586)
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.set_count = 3
        self.reserve = Supboard(self.user, self.start_date, self.start_time,
                                set_count=3, count=2)

    def drop_table(self):
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS sup_reserves")

        self.connection.commit()

    async def test_append_data(self):
        self.reserve.user.firstname = "1111"
        supboard1 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "2222"
        supboard2 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "3333"
        supboard3 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "4444"
        supboard4 = self.adapter.append_data(self.reserve)

        passed, alert = self.assert_params(supboard1.id, 1)
        assert passed, alert

        passed, alert = self.assert_params(supboard2.id, 2)
        assert passed, alert

        passed, alert = self.assert_params(supboard3.id, 3)
        assert passed, alert

        passed, alert = self.assert_params(supboard4.id, 4)
        assert passed, alert

    async def test_get_data(self):
        supboards = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            supboards.append(self.adapter.append_data(self.reserve))

        rows = self.adapter.get_data()

        for row, supboard in zip(rows, supboards):
            passed, alert = self.assert_params(row.id, supboard.id)
            assert passed, alert

    async def test_get_active_reserves(self):
        supboards = []
        self.reserve.start_time = time(datetime.today().time().hour + 1)
        for i in range(8):
            self.reserve.user.firstname = str(i)*5
            self.reserve.start_date = date.today() + timedelta(i - 2)
            supboards.append(self.adapter.append_data(self.reserve))

        rows = list(self.adapter.get_active_reserves())
        passed, alert = self.assert_params(len(rows), 6)
        assert passed, alert

        for i in range(2, 8):
            passed, alert = self.assert_params(rows[i - 2], supboards[i])
            assert passed, alert

    async def test_get_data_by_keys(self):
        supboards = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            supboards.append(self.adapter.append_data(self.reserve))

        for supboard in supboards:
            passed, alert = self.assert_params(
                self.adapter.get_data_by_keys(supboard.id).id, supboard.id)
            assert passed, alert

    async def test_update_data(self):
        supboards = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            supboards.append(self.adapter.append_data(self.reserve))

        supboards[1].set_count = 3
        self.adapter.update_data(supboards[1])

        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(supboards[1].id).set_count, 3)
        assert passed, alert

    async def test_remove_data_by_keys(self):
        supboards = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            supboards.append(self.adapter.append_data(self.reserve))

        self.adapter.remove_data_by_keys(supboards[2].id)
        rows = list(self.adapter.get_data())

        passed, alert = self.assert_params(len(rows), 3)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(supboards[2].id), None)
        assert passed, alert

    async def test_get_concurrent_reserves(self):

        self.supboards = []
        for i in range(8):
            start_time = time(10 + i)
            user = User(f"Firstname{i}")
            user.lastname = f"Lastname{i}"
            user.telegram_id = int(str(i)*8)
            start_date = date.today()
            supboard = Supboard(user, start_date=start_date,
                                start_time=start_time,
                                set_count=(i + 1), count=(i % 3))
            self.supboards.append(supboard)
            self.adapter.append_data(supboard)

        supboard = self.supboards[1]
        supboard.set_count = 3
        rows = list(self.adapter.get_concurrent_reserves(self.supboards[1]))

        passed, alert = self.assert_params(len(rows), 2)
        assert passed, alert

    async def test_get_concurrent_count(self):

        self.supboards = []

        for i in range(8):
            start_time = time(10 + i)
            user = User(f"Firstname{i}")
            user.lastname = f"Lastname{i}"
            user.telegram_id = int(str(i)*8)
            start_date = date.today()
            supboard = Supboard(user, start_date=start_date,
                                start_time=start_time,
                                set_count=(i + 1), count=(i % 3))
            self.supboards.append(supboard)
            self.adapter.append_data(supboard)

        supboard = self.supboards[1]
        supboard.set_count = 3
        count = self.adapter.get_concurrent_count(self.supboards[1])

        passed, alert = self.assert_params(count, 3)
        assert passed, alert
