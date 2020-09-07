import psycopg2

from copy import deepcopy
from datetime import datetime
from typing import Union

from ..data import ReserveDataAdapter
from ...entities import Supboard, User


class PostgressSupboardAdapter(ReserveDataAdapter):
    """Supboard PostgreSQL data adapter class

    Attributes:
        connection:
            A PostgreSQL connection instance.
    """
    _columns = (
        "id", "firstname", "lastname", "middlename", "displayname",
        "telegram_id", "phone_number", "start_time", "end_time",
        "set_type_id", "set_count", "count", "canceled")

    def __init__(self,
                 connection=None, database_url=None,
                 table_name="sup_reserves"):
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
                """ (
                    id SERIAL PRIMARY KEY,
                    telegram_id integer,
                    firstname varchar(20),
                    lastname varchar(20),
                    middlename varchar(20),
                    displayname varchar(60),
                    phone_number varchar(20),
                    start_time timestamp,
                    end_time timestamp,
                    set_type_id varchar(20),
                    set_count integer,
                    count integer,
                    canceled boolean DEFAULT false,
                    cancel_telegram_id integer)""")

        self._connection.commit()

    def get_supboard_from_row(self, row):
        supboard_id = row[self._columns.index("id")]
        user = User(row[self._columns.index("firstname")])
        user.lastname = row[self._columns.index("lastname")]
        user.middlename = row[self._columns.index("middlename")]
        user.displayname = row[self._columns.index("displayname")]
        user.telegram_id = row[self._columns.index("telegram_id")]
        user.phone_number = row[self._columns.index("phone_number")]
        start = row[self._columns.index("start_time")]
        set_type_id = row[self._columns.index("set_type_id")]
        set_count = row[self._columns.index("set_count")]
        count = row[self._columns.index("count")]
        canceled = row[self._columns.index("canceled")]

        return Supboard(id=supboard_id, user=user,
                        start_date=start.date(), start_time=start.time(),
                        set_type_id=set_type_id, set_count=set_count,
                        count=count, canceled=canceled)

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
                yield self.get_supboard_from_row(row)

    def get_active_reserves(self) -> iter:
        """Get an active supboard reservations from storage

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute((f"SELECT {columns_str} FROM {self._table_name}"
                            " WHERE NOT canceled and start_time >= %s"
                            " ORDER BY start_time"), [datetime.today()])

            self._connection.commit()

            for row in cursor:
                yield self.get_supboard_from_row(row)

    def get_data_by_keys(self, id: int) -> Union[Supboard, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of Supboard reservation

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute((f"SELECT {columns_str} FROM {self._table_name}"
                            " WHERE id = %s"), [id])

            self._connection.commit()

            rows = list(cursor)
            if len(rows) == 0:
                return None

            row = rows[0]
            return self.get_supboard_from_row(row)

    def get_concurrent_reserves(self, reserve: Supboard) -> iter:
        """Get an concurrent reservations from storage

        Returns:
            A iterator object of given data
        """
        start_ts = reserve.start
        end_ts = reserve.end

        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns)
            cursor.execute(f"SELECT {columns_str} FROM {self._table_name}"
                           " WHERE NOT canceled"
                           "       and ((%s = start_time)"
                           "       or (%s < start_time and %s > start_time)"
                           "       or (%s > start_time and %s < end_time))"
                           " ORDER BY start_time",
                           (start_ts, start_ts, end_ts, start_ts, start_ts))

            self._connection.commit()

            for row in cursor:
                yield self.get_supboard_from_row(row)

    def get_concurrent_count(self, reserve: Supboard) -> int:
        """Get an concurrent reservations count from storage

        Returns:
            An integer count of concurrent reservations
        """
        start_ts = reserve.start
        end_ts = reserve.end

        with self._connection.cursor() as cursor:
            cursor.execute(
                "   SELECT SUM(count) AS concurrent_count"
                f"  FROM {self._table_name}"
                """ WHERE NOT canceled
                        and ((%s = start_time)
                        or (%s < start_time and %s > start_time)
                        or (%s > start_time and %s < end_time))""",
                (start_ts, start_ts, end_ts, start_ts, start_ts))

            self._connection.commit()

            if cursor:
                row = list(cursor)
            else:
                return 0

            return row[0][0] if row[0][0] else 0

    def append_data(self, reserve: Supboard) -> Supboard:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity Supboard class.
        """
        with self._connection.cursor() as cursor:
            columns_str = ", ".join(self._columns[1:])
            cursor.execute(
                f"  INSERT INTO {self._table_name} ({columns_str})"
                "    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                "    RETURNING id", (
                    reserve.user.firstname,
                    reserve.user.lastname,
                    reserve.user.middlename,
                    reserve.user.displayname,
                    reserve.user.telegram_id,
                    reserve.user.phone_number,
                    reserve.start,
                    reserve.end,
                    reserve.set_type.set_id,
                    reserve.set_count,
                    reserve.count,
                    reserve.canceled
                ))

            result = deepcopy(reserve)
            result.id = cursor.fetchone()[0]

            self._connection.commit()

            return result

    def update_data(self, reserve: Supboard):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity Supboard class.
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"  UPDATE {self._table_name} SET"
                """     firstname = %s, lastname = %s, middlename = %s,
                        displayname = %s, phone_number = %s, telegram_id = %s,
                        start_time = %s, end_time = %s, set_type_id = %s,
                        set_count = %s, count = %s,
                        canceled = %s, cancel_telegram_id = %s"""
                "   WHERE id = %s", (
                    reserve.user.firstname,
                    reserve.user.lastname,
                    reserve.user.middlename,
                    reserve.user.displayname,
                    reserve.user.phone_number,
                    reserve.user.telegram_id,
                    reserve.start,
                    reserve.end,
                    reserve.set_type.set_id,
                    reserve.set_count,
                    reserve.count,
                    reserve.canceled,
                    reserve.cancel_telegram_id,
                    reserve.id))

            self._connection.commit()

    def remove_data_by_keys(self, id: int):
        """Remove data from storage by a keys

        Args:
            id:
                An identifier of Supboard reservation

        Returns:
            A iterator object of given data
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self._table_name} WHERE id = %s", [id])
            self._connection.commit()
