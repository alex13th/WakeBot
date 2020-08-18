import os
import psycopg2
from ...base_test_case import BaseTestCase
from wakebot.adapters.postgres import PostgresUserAdapter
from wakebot.entities import User


class PostgresUserAdapterTestCase(BaseTestCase):
    """PostgresUserAdapter class"""
    def __init__(self):
        super().__init__()
        DATABASE_URL = os.environ["DATABASE_URL"]
        self.connection = psycopg2.connect(DATABASE_URL)

    def setUp(self):
        self.drop_table()
        self.adapter = PostgresUserAdapter(self.connection)
        self.user = User(
            firstname="Firstname",
            lastname="Lastname",
            middlename="Middlename",
            phone_number="914",
            telegram_id=586)

    def drop_table(self):
        cursor = self.connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS users")

        self.connection.commit()

    async def test_append_data(self):
        self.user.firstname = "Firstname1111"
        self.user.telegram_id = "1111"
        user1 = self.adapter.append_data(self.user)

        self.user.firstname = "Firstname222"
        self.user.telegram_id = "2222"
        user2 = self.adapter.append_data(self.user)

        self.user.firstname = "Firstname3333"
        self.user.telegram_id = "3333"
        user3 = self.adapter.append_data(self.user)

        self.user.firstname = "Firstname4444"
        self.user.telegram_id = "4444"
        user4 = self.adapter.append_data(self.user)

        passed, alert = self.assert_params(user1.user_id, 1)
        assert passed, alert

        passed, alert = self.assert_params(user2.user_id, 2)
        assert passed, alert

        passed, alert = self.assert_params(user3.user_id, 3)
        assert passed, alert

        passed, alert = self.assert_params(user4.user_id, 4)
        assert passed, alert

    async def test_get_data(self):
        users = []
        for i in range(4):
            self.user.firstname = str(i)*5
            self.user.telegram_id = str(i)*5
            users.append(self.adapter.append_data(self.user))

        rows = self.adapter.get_data()

        for row, user in zip(rows, users):
            passed, alert = self.assert_params(row.user_id, user.user_id)
            assert passed, alert

    async def test_get_data_by_keys(self):
        users = []
        for i in range(4):
            self.user.firstname = str(i)*5
            self.user.telegram_id = str(i)*5
            users.append(self.adapter.append_data(self.user))

        for user in users:
            passed, alert = self.assert_params(
                self.adapter.get_data_by_keys(user.user_id).user_id,
                user.user_id)
            assert passed, alert

    async def test_user_by_telegram_id(self):
        users = []
        for i in range(4):
            self.user.firstname = str(i)*5
            self.user.telegram_id = int(str(i)*5)
            users.append(self.adapter.append_data(self.user))

        for user in users:
            dbuser = self.adapter.get_user_by_telegram_id(user.telegram_id)
            passed, alert = self.assert_params(
                dbuser.telegram_id,
                user.telegram_id)
            assert passed, alert

    async def test_update_data(self):
        users = []
        for i in range(4):
            self.user.firstname = str(i)*5
            self.user.telegram_id = str(i)*5
            users.append(self.adapter.append_data(self.user))

        users[1].lastname = "NewLastname"
        self.adapter.update_data(users[1])

        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(users[1].user_id).lastname,
            "NewLastname")
        assert passed, alert

    async def test_remove_data_by_keys(self):
        users = []
        for i in range(4):
            self.user.firstname = str(i)*5
            self.user.telegram_id = str(i)*5
            users.append(self.adapter.append_data(self.user))

        self.adapter.remove_data_by_keys(users[2].user_id)
        rows = list(self.adapter.get_data())

        passed, alert = self.assert_params(len(rows), 3)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys(users[2].user_id), None)
        assert passed, alert
