import psycopg2

from copy import deepcopy
from typing import Union

from ..data import UserDataAdapter
from ...entities.user import User


class PostgresUserAdapter(UserDataAdapter):
    """Wakeboard SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """
    _columns = (
        "id", "firstname", "lastname", "middlename", "displayname",
        "telegram_id", "phone_number", "is_admin")

    def __init__(self,
                 connection=None, database_url=None,
                 table_name="users"):
        self._connection = connection
        self.__database_url = database_url
        self._table_name = table_name

        self.connect()
        self.create_table()

    @property
    def connection(self):
        return self._connection

    def connect(self):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            self._connection = psycopg2.connect(self.__database_url)

    def create_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self._table_name}"
                """ (id SERIAL PRIMARY KEY,
                    firstname varchar(20),
                    lastname varchar(20),
                    middlename varchar(20),
                    displayname varchar(60),
                    telegram_id integer,
                    phone_number varchar(20),
                    is_admin boolean)""")

            self.connection.commit()

    def get_user_from_row(self, row):
        user_id = row[self._columns.index("id")]
        firstname = row[self._columns.index("firstname")]
        lastname = row[self._columns.index("lastname")]
        middlename = row[self._columns.index("middlename")]
        displayname = row[self._columns.index("displayname")]
        telegram_id = row[self._columns.index("telegram_id")]
        phone_number = row[self._columns.index("phone_number")]
        is_admin = row[self._columns.index("is_admin")]

        return User(user_id=user_id, firstname=firstname, lastname=lastname,
                    middlename=middlename, displayname=displayname,
                    telegram_id=telegram_id, phone_number=phone_number,
                    is_admin=is_admin)

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute(f"SELECT {columns_str} FROM {self._table_name}")

            self._connection.commit()

            for row in cursor:
                yield self.get_user_from_row(row)

    def get_data_by_keys(self, id: int) -> Union[User, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of user

        Returns:
            A object of given data
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute(f"SELECT {columns_str} FROM {self._table_name}"
                           " WHERE id = %s", [id])

            self._connection.commit()

            rows = list(cursor)
            if len(rows) == 0:
                return None

            row = rows[0]
            cursor.close()
            return self.get_user_from_row(row)

    def get_user_by_telegram_id(self, telegram_id: int) -> Union[User, None]:
        """Get a user from storage by telegram_id

        Args:
            telegram_id:
                An telegram identifier of user

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute(f"SELECT {columns_str} FROM {self._table_name}"
                           " WHERE telegram_id = %s", [telegram_id])

            self._connection.commit()

            rows = list(cursor)
            if len(rows) == 0:
                return None

            row = rows[0]
            cursor.close()
            return self.get_user_from_row(row)

    def get_admins(self) -> iter:
        """Get administrators list from storage

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute(f"SELECT {columns_str} FROM {self._table_name}"
                           " WHERE is_admin")

            self._connection.commit()

            for row in cursor:
                yield self.get_user_from_row(row)

    def append_data(self, user: User) -> User:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"  INSERT INTO {self._table_name}("
                """     telegram_id, firstname, lastname, middlename,
                        displayname, phone_number, is_admin)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    user.telegram_id,
                    user.firstname,
                    user.lastname,
                    user.middlename,
                    user.displayname,
                    user.phone_number,
                    user.is_admin)
            )

            result = deepcopy(user)
            result.user_id = cursor.fetchone()[0]

            self._connection.commit()

            return result

    def update_data(self, user: User):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"  UPDATE {self._table_name} SET "
                """     firstname = %s, lastname = %s, middlename = %s,
                        displayname = %s, phone_number = %s,
                        telegram_id = %s, is_admin = %s
                    WHERE id = %s
                """, (
                    user.firstname,
                    user.lastname,
                    user.middlename,
                    user.displayname,
                    user.phone_number,
                    user.telegram_id,
                    user.is_admin,
                    user.user_id
                ))

            self._connection.commit()

    def remove_data_by_keys(self, id: int):
        """Remove data from storage by a keys

        Args:
            id:
                An identifier of wake reservation

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self._table_name} WHERE id = %s", [id])

            self._connection.commit()
