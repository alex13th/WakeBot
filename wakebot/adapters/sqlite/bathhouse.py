from copy import deepcopy
from datetime import datetime
from sqlite3 import Connection
from typing import Union

from ..data import ReserveDataAdapter
from ...entities import Bathhouse, User


class SqliteBathhouseAdapter(ReserveDataAdapter):
    """Bathhouse SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """
    _columns = (
        "id", "firstname", "lastname", "middlename", "displayname",
        "telegram_id", "phone_number", "start", "end",
        "set_type_id", "set_count", "count", "canceled")

    def __init__(self, connection: Connection,
                 table_name="bathhouse_reserves"):
        self._connection = connection
        self._table_name = table_name
        self.create_table()

    @property
    def connection(self):
        return self._connection

    def create_table(self):
        cursor = self._connection.cursor()

        cursor.execute(
            f"  CREATE TABLE IF NOT EXISTS {self._table_name} ("
            """     id integer PRIMARY KEY AUTOINCREMENT,
                    telegram_id integer,
                    firstname text,
                    lastname text,
                    middlename text,
                    displayname text,
                    phone_number text,
                    start TIMESTAMP,
                    end TIMESTAMP,
                    set_type_id text,
                    set_count integer,
                    count integer,
                    canceled integer DEFAULT 0, cancel_telegram_id integer)
            """)

        self.connection.commit()

    def get_bathhouse_from_row(self, row):
        bathhouse_id = row[self._columns.index("id")]
        user = User(row[self._columns.index("firstname")])
        user.lastname = row[self._columns.index("lastname")]
        user.middlename = row[self._columns.index("middlename")]
        user.displayname = row[self._columns.index("displayname")]
        user.telegram_id = row[self._columns.index("telegram_id")]
        user.phone_number = row[self._columns.index("phone_number")]
        start = datetime.fromtimestamp(row[self._columns.index("start")])
        set_type_id = row[self._columns.index("set_type_id")]
        set_count = row[self._columns.index("set_count")]
        count = row[self._columns.index("count")]
        canceled = row[self._columns.index("canceled")]

        return Bathhouse(id=bathhouse_id, user=user,
                         start_date=start.date(), start_time=start.time(),
                         set_type_id=set_type_id, set_count=set_count,
                         count=count, canceled=canceled)

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        cursor = self._connection.cursor()
        columns_str = ", ".join(self._columns)
        cursor.execute(f"SELECT {columns_str} FROM {self._table_name}")

        for row in cursor:
            yield self.get_bathhouse_from_row(row)

    def get_active_reserves(self) -> iter:
        """Get an active Bathhouse reservations from storage

        Returns:
            A iterator object of given data
        """
        cursor = self._connection.cursor()
        columns_str = ", ".join(self._columns)
        cursor.execute(
            f"SELECT {columns_str} FROM {self._table_name}"
            " WHERE NOT canceled and start >= ?"
            " ORDER BY start", [datetime.today().timestamp()])

        for row in cursor:
            yield self.get_bathhouse_from_row(row)

    def get_data_by_keys(self, id: int) -> Union[Bathhouse, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of Bathhouse reservation

        Returns:
            A iterator object of given data
        """
        cursor = self._connection.cursor()
        columns_str = ", ".join(self._columns)
        rows = list(cursor.execute(
            f"SELECT {columns_str} FROM {self._table_name}"
            " WHERE id = ?", [id]))

        if len(rows) == 0:
            return None
        else:
            return self.get_bathhouse_from_row(rows[0])

    def get_concurrent_reserves(self, reserve: Bathhouse) -> iter:
        """Get an concurrent reservations from storage

        Returns:
            A iterator object of given data
        """

        start_ts = reserve.start.timestamp()
        end_ts = reserve.end.timestamp()
        cursor = self._connection.cursor()
        columns_str = ", ".join(self._columns)
        cursor.execute(
            f"SELECT {columns_str} FROM {self._table_name}"
            " WHERE NOT canceled"
            "       and ((? = start) or (? < start and ? > start)"
            "       or (? > start and ? < end))"
            " ORDER BY start",
            (start_ts, start_ts, end_ts, start_ts, start_ts))

        for row in cursor:
            yield self.get_bathhouse_from_row(row)

    def get_concurrent_count(self, reserve: Bathhouse) -> int:
        """Get an concurrent reservations count from storage

        Returns:
            An integer count of concurrent reservations
        """

        start_ts = reserve.start.timestamp()
        end_ts = reserve.end.timestamp()
        cursor = self._connection.cursor()
        cursor = cursor.execute(
            "   SELECT SUM(count) AS concurrent_count"
            f"  FROM {self._table_name}"
            """ WHERE NOT canceled
                    and ((? = start) or (? < start and ? > start) or
                    (? > start and ? < end))
                ORDER BY start""",
            (start_ts, start_ts, end_ts, start_ts, start_ts))

        row = list(cursor)
        return row[0][0] if row[0][0] else 0

    def append_data(self, reserve: Bathhouse) -> Bathhouse:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity Bathhouse class.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            f"  INSERT INTO {self._table_name} ("
            """     telegram_id, firstname, lastname,
                    middlename, displayname, phone_number,
                    start, end, set_type_id, set_count, count)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reserve.user.telegram_id,
                reserve.user.firstname,
                reserve.user.lastname,
                reserve.user.middlename,
                reserve.user.displayname,
                reserve.user.phone_number,
                reserve.start.timestamp(),
                reserve.end.timestamp(),
                reserve.set_type.set_id,
                reserve.set_count,
                reserve.count
            ))
        self._connection.commit()

        result = deepcopy(reserve)
        result.id = cursor.lastrowid

        return result

    def update_data(self, reserve: Bathhouse):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity Bathhouse class.
        """
        cursor = self._connection.cursor()
        cursor = cursor.execute(
            f"  UPDATE {self._table_name} SET"
            """     firstname = ?, lastname = ?, middlename = ?, displayname = ?,
                    phone_number = ?, telegram_id = ?, start = ?, end = ?,
                    set_type_id = ?, set_count = ?, count = ?,
                    canceled = ?, cancel_telegram_id = ?
                WHERE id = ?
           """, (
                reserve.user.firstname,
                reserve.user.lastname,
                reserve.user.middlename,
                reserve.user.displayname,
                reserve.user.phone_number,
                reserve.user.telegram_id,
                reserve.start.timestamp(),
                reserve.end.timestamp(),
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
                An identifier of Bathhouse reservation

        Returns:
            A iterator object of given data
        """
        cursor = self._connection.cursor()
        cursor = cursor.execute(
            f" DELETE FROM {self._table_name} WHERE id = ?", [id])
        self._connection.commit()
