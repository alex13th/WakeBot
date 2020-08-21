from sqlite3 import Connection
from datetime import datetime
from typing import Union
from ..data import ReserveDataAdapter
from ...entities.wake import Wake
from ...entities.user import User


class SqliteWakeAdapter(ReserveDataAdapter):
    """Wakeboard SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """

    def __init__(self, connection: Connection, table_name="wake_reserves"):
        self.__connection = connection
        self.__table_name = table_name
        self.create_table()

    @property
    def connection(self):
        return self.__connection

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, start, set_type_id, set_count, board, hydro"""
            f"  FROM {self.__table_name}")
        for row in cursor:
            user = User(row[1])
            user.lastname = row[2]
            user.middlename = row[3]
            user.displayname = row[4]
            user.telegram_id = row[5]
            start = datetime.fromtimestamp(row[6])

            yield Wake(
                id=row[0], user=user,
                start_date=start.date(), start_time=start.time(),
                set_type_id=row[7], set_count=row[8],
                board=row[9], hydro=row[10])

    def get_active_reserves(self) -> iter:
        """Get an active wakeboard reservations from storage

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, start, set_type_id, set_count, board, hydro"""
            f"  FROM {self.__table_name}"
            """ WHERE start >= ?
                ORDER BY start""", [datetime.today().timestamp()])
        for row in cursor:
            user = User(row[1])
            user.lastname = row[2]
            user.middlename = row[3]
            user.displayname = row[4]
            user.telegram_id = row[5]
            start = datetime.fromtimestamp(row[6])

            yield Wake(
                id=row[0], user=user,
                start_date=start.date(), start_time=start.time(),
                set_type_id=row[7], set_count=row[8],
                board=row[9], hydro=row[10])

    def get_data_by_keys(self, id: int) -> Union[Wake, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of wake reservation

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        rows = list(cursor.execute(
            """SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, phone_number, start, set_type_id, set_count,
                    board, hydro"""
            f" FROM {self.__table_name} WHERE id = ?", [id]))

        if len(rows) == 0:
            return None

        row = rows[0]
        user = User(row[1])
        user.lastname = row[2]
        user.middlename = row[3]
        user.displayname = row[4]
        user.telegram_id = row[5]
        user.phone_number = row[6]
        start = datetime.fromtimestamp(row[7])

        return Wake(
            id=row[0], user=user,
            start_date=start.date(), start_time=start.time(),
            set_type_id=row[8], set_count=row[9],
            board=row[10], hydro=row[11])

    def get_concurrent_reserves(self, reserve: Wake) -> iter:
        """Get an concurrent reservations from storage

        Returns:
            A iterator object of given data
        """

        start_ts = reserve.start.timestamp()
        end_ts = reserve.end.timestamp()
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, phone_number, start, end,
                    set_type_id, set_count, board, hydro, count"""
            f"  FROM {self.__table_name}"
            """ WHERE (? = start) or (? < start and ? > start) or
                      (? > start and ? < end)
                ORDER BY start""",
            (start_ts, start_ts, end_ts, start_ts, start_ts))

        for row in cursor:
            user = User(row[1])
            user.lastname = row[2]
            user.middlename = row[3]
            user.displayname = row[4]
            user.telegram_id = row[5]
            user.phone_number = row[6]
            start = datetime.fromtimestamp(row[7]) if row[7] else None
            start_date = start.date() if start else None
            start_time = start.time() if start else None
            _ = datetime.fromtimestamp(row[8])

            yield Wake(
                id=row[0], user=user,
                start_date=start_date, start_time=start_time,
                set_type_id=row[9], set_count=row[10],
                board=row[11], hydro=row[12])

    def get_concurrent_count(self, reserve: Wake) -> int:
        """Get an concurrent reservations count from storage

        Returns:
            An integer count of concurrent reservations
        """

        start_ts = reserve.start.timestamp()
        end_ts = reserve.end.timestamp()
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            "   SELECT SUM(count) AS concurrent_count"
            f"  FROM {self.__table_name}"
            """ WHERE (? = start) or (? < start and ? > start) or
                      (? > start and ? < end)
                ORDER BY start""",
            (start_ts, start_ts, end_ts, start_ts, start_ts))

        row = list(cursor)
        return row[0][0] if row[0][0] else 0

    def append_data(self, reserve: Wake) -> Wake:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        cursor = self.__connection.cursor()
        cursor.execute(
            f"  INSERT INTO {self.__table_name} ("
            """     telegram_id, firstname, lastname,
                    middlename, displayname, phone_number,
                    start, end, set_type_id, set_count, board, hydro, count)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                reserve.board,
                reserve.hydro,
                reserve.count
            ))
        self.__connection.commit()

        result = reserve.__deepcopy__()
        result.id = cursor.lastrowid

        return result

    def update_data(self, reserve: Wake):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            f"  UPDATE {self.__table_name} SET"
            """     firstname = ?, lastname = ?, middlename = ?, displayname = ?,
                    phone_number = ?, telegram_id = ?, start = ?, end = ?,
                    set_type_id = ?, set_count = ?,
                    board = ?, hydro = ?, count = ?
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
                reserve.board,
                reserve.hydro,
                reserve.count,
                reserve.id
            ))
        self.__connection.commit()

    def remove_data_by_keys(self, id: int):
        """Remove data from storage by a keys

        Args:
            id:
                An identifier of wake reservation

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            f" DELETE FROM {self.__table_name} WHERE id = ?", [id])
        self.__connection.commit()

    def create_table(self):
        cursor = self.__connection.cursor()

        cursor.execute(
            f"  CREATE TABLE IF NOT EXISTS {self.__table_name} ("
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
                    board integer, hydro integer, count integer)
            """)

        self.connection.commit()
