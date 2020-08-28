import sqlite3
from datetime import datetime, date, time, timedelta
from ...base_test_case import BaseTestCase
from wakebot.adapters.sqlite import SqliteBathhouseAdapter
from wakebot.entities import Bathhouse, User


class SqliteBathhouseAdapterTestCase(BaseTestCase):
    """SqliteBathhouseAdapter class"""
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("bot_tests/data/sqlite/wake.db")

    def setUp(self):
        self.drop_table()
        self.adapter = SqliteBathhouseAdapter(self.connection)
        self.user = User("Firstname", telegram_id=586, phone_number="+77777")
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.set_count = 3
        self.reserve = Bathhouse(self.user, self.start_date, self.start_time,
                                 set_count=3, count=2)

    def drop_table(self):
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS bathhouse_reserves")

        self.connection.commit()

    async def test_append_data(self):
        self.reserve.user.firstname = "1111"
        bathhouse1 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "2222"
        bathhouse2 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "3333"
        bathhouse3 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "4444"
        bathhouse4 = self.adapter.append_data(self.reserve)

        passed, alert = self.assert_params(bathhouse1.id, 1)
        assert passed, alert

        passed, alert = self.assert_params(bathhouse2.id, 2)
        assert passed, alert

        passed, alert = self.assert_params(bathhouse3.id, 3)
        assert passed, alert

        passed, alert = self.assert_params(bathhouse4.id, 4)
        assert passed, alert

    async def test_get_data(self):
        bathhouses = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            bathhouses.append(self.adapter.append_data(self.reserve))

        rows = self.adapter.get_data()

        for row, bathhouse in zip(rows, bathhouses):
            passed, alert = self.assert_params(row.id, bathhouse.id)
            assert passed, alert

    async def test_get_active_reserves(self):
        bathhouses = []
        self.reserve.start_time = time(datetime.today().time().hour + 1)
        for i in range(8):
            self.reserve.user.firstname = str(i)*5
            self.reserve.start_date = date.today() + timedelta(i - 2)
            bathhouses.append(self.adapter.append_data(self.reserve))

        rows = list(self.adapter.get_active_reserves())
        passed, alert = self.assert_params(len(rows), 6)
        assert passed, alert

        for i in range(2, 8):
            passed, alert = self.assert_params(rows[i - 2], bathhouses[i])
            assert passed, alert

    async def test_get_data_by_keys(self):
        bathhouses = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            bathhouses.append(self.adapter.append_data(self.reserve))

        for bathhouse in bathhouses:
            passed, alert = self.assert_params(
                self.adapter.get_data_by_keys(bathhouse.id).id, bathhouse.id)
            assert passed, alert

    async def test_update_data(self):
        bathhouses = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            bathhouses.append(self.adapter.append_data(self.reserve))

        bathhouses[1].set_count = 3
        self.adapter.update_data(bathhouses[1])

        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(bathhouses[1].id).set_count, 3)
        assert passed, alert

    async def test_remove_data_by_keys(self):
        bathhouses = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            bathhouses.append(self.adapter.append_data(self.reserve))

        self.adapter.remove_data_by_keys(bathhouses[2].id)
        rows = list(self.adapter.get_data())

        passed, alert = self.assert_params(len(rows), 3)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(bathhouses[2].id), None)
        assert passed, alert

    async def test_get_concurrent_reserves(self):

        self.bathhouses = []
        for i in range(8):
            start_time = time(10 + i)
            user = User(f"Firstname{i}", phone_number="+7777")
            user.lastname = f"Lastname{i}"
            user.telegram_id = int(str(i)*8)
            start_date = date.today()
            bathhouse = Bathhouse(user, start_date=start_date,
                                  start_time=start_time,
                                  set_count=(i + 1), count=(i % 3))
            self.bathhouses.append(bathhouse)
            self.adapter.append_data(bathhouse)

        bathhouse = self.bathhouses[1]
        bathhouse.set_count = 3
        rows = list(self.adapter.get_concurrent_reserves(self.bathhouses[1]))

        passed, alert = self.assert_params(len(rows), 3)
        assert passed, alert

    async def test_get_concurrent_count(self):

        self.bathhouses = []

        for i in range(8):
            start_time = time(10 + i)
            user = User(f"Firstname{i}", phone_number="+7777")
            user.lastname = f"Lastname{i}"
            user.telegram_id = int(str(i)*8)
            start_date = date.today()
            bathhouse = Bathhouse(user, start_date=start_date,
                                  start_time=start_time,
                                  set_count=(i + 1), count=(i % 3))
            self.bathhouses.append(bathhouse)
            self.adapter.append_data(bathhouse)

        bathhouse = self.bathhouses[1]
        bathhouse.set_count = 3
        count = self.adapter.get_concurrent_count(self.bathhouses[1])

        passed, alert = self.assert_params(count, 3)
        assert passed, alert
