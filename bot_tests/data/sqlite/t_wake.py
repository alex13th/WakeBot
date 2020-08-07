import sqlite3
from datetime import date, time
from ...base_test_case import BaseTestCase
from wakebot.adapters.sqlite.wake import SqliteWakeAdapter
from wakebot.entities.wake import Wake
from wakebot.entities.user import User


class SqliteWakeAdapterTestCase(BaseTestCase):

    def setUp(self):
        self.connection = sqlite3.connect("bot_tests/data/sqlite/wake.db")
        self.drop_table()
        self.adapter = SqliteWakeAdapter(self.connection)

        self.user = User("Firstname", telegram_id=586)
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.set_count = 3
        self.reserve = Wake(self.user, self.start_date, self.start_time,
                            set_count=3, board=1, hydro=1)

    def drop_table(self):
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS wake")

        self.connection.commit()

    async def test_append_data(self):
        self.reserve.user.firstname = "1111"
        wake1 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "2222"
        wake2 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "3333"
        wake3 = self.adapter.append_data(self.reserve)
        self.reserve.user.firstname = "4444"
        wake4 = self.adapter.append_data(self.reserve)

        passed, alert = self.assert_params(wake1.id, 1)
        assert passed, alert

        passed, alert = self.assert_params(wake2.id, 2)
        assert passed, alert

        passed, alert = self.assert_params(wake3.id, 3)
        assert passed, alert

        passed, alert = self.assert_params(wake4.id, 4)
        assert passed, alert

    async def test_get_data(self):
        wakes = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            wakes.append(self.adapter.append_data(self.reserve))

        rows = self.adapter.get_data()

        for row, wake in zip(rows, wakes):
            passed, alert = self.assert_params(row.id, wake.id)
            assert passed, alert

    async def test_get_data_by_keys(self):
        wakes = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            wakes.append(self.adapter.append_data(self.reserve))

        for wake in wakes:
            passed, alert = self.assert_params(
                self.adapter.get_data_by_keys(wake.id).id, wake.id)
            assert passed, alert

    async def test_update_data(self):
        wakes = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            wakes.append(self.adapter.append_data(self.reserve))

        wakes[1].set_count = 3
        self.adapter.update_data(wakes[1])

        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(wakes[1].id).set_count, 3)
        assert passed, alert

    async def test_remove_data_by_keys(self):
        wakes = []
        for i in range(4):
            self.reserve.user.firstname = str(i)*5
            wakes.append(self.adapter.append_data(self.reserve))

        self.adapter.remove_data_by_keys(wakes[2].id)
        rows = list(self.adapter.get_data())

        passed, alert = self.assert_params(len(rows), 3)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(wakes[2].id), None)
        assert passed, alert
