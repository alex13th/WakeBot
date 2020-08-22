import os
import psycopg2
from datetime import datetime, date, time, timedelta
from ...base_test_case import BaseTestCase
from wakebot.adapters.postgres import PostgressWakeAdapter
from wakebot.entities import Wake, User


class PostgresWakeAdapterTestCase(BaseTestCase):
    """PostgresWakeAdapter class"""
    def __init__(self):
        super().__init__()
        DATABASE_URL = os.environ["DATABASE_URL"]
        self.connection = psycopg2.connect(DATABASE_URL)

    def setUp(self):
        self.drop_table()
        self.adapter = PostgressWakeAdapter(self.connection)
        self.user = User("Firstname", telegram_id=586, phone_number="+777")
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.set_count = 3
        self.reserve = Wake(self.user, self.start_date, self.start_time,
                            set_count=3, board=1, hydro=1)

    def drop_table(self):
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS wake_reserves")

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

    async def test_get_active_reserves(self):
        wakes = []
        self.reserve.start_time = time(datetime.today().time().hour + 1)
        for i in range(8):
            self.reserve.user.firstname = str(i)*5
            self.reserve.start_date = date.today() + timedelta(i - 2)
            wakes.append(self.adapter.append_data(self.reserve))

        rows = list(self.adapter.get_active_reserves())
        passed, alert = self.assert_params(len(rows), 6)
        assert passed, alert

        for i in range(2, 8):
            passed, alert = self.assert_params(rows[i - 2], wakes[i])
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

    async def test_get_concurrent_reserves(self):

        self.wakes = []
        for i in range(8):
            start_time = time(10 + i)
            user = User(f"Firstname{i}", phone_number="+7777")
            user.lastname = f"Lastname{i}"
            user.telegram_id = int(str(i)*8)
            start_date = date.today()
            wake = Wake(user, start_date=start_date, start_time=start_time,
                        set_count=(i + 1))
            wake.board = i % 2
            wake.hydro = i % 3
            self.wakes.append(wake)
            self.adapter.append_data(wake)

        wake = self.wakes[1]
        wake.set_count = 10
        rows = list(self.adapter.get_concurrent_reserves(self.wakes[1]))

        passed, alert = self.assert_params(len(rows), 2)
        assert passed, alert

    async def test_get_concurrent_count(self):

        self.wakes = []
        for i in range(8):
            start_time = time(10 + i)
            user = User(f"Firstname{i}", phone_number="+777")
            user.lastname = f"Lastname{i}"
            user.telegram_id = int(str(i)*8)
            start_date = date.today()
            wake = Wake(user, start_date=start_date, start_time=start_time,
                        set_count=(i + 1))
            wake.board = i % 2
            wake.hydro = i % 3
            self.wakes.append(wake)
            self.adapter.append_data(wake)

        wake = self.wakes[1]
        wake.set_count = 10
        count = self.adapter.get_concurrent_count(self.wakes[1])

        passed, alert = self.assert_params(count, 2)
        assert passed, alert
