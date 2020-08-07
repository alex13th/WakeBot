from sqlite3 import Connection
from datetime import datetime
from typing import Union
from ..data import WakeDataAdapter
from ...entities.wake import Wake
from ...entities.user import User


class SqliteWakeAdapter(WakeDataAdapter):
    """Wakeboard SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """

    def __init__(self, connection: Connection):
        self.__connection = connection
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
            """SELECT
                id, firstname, lastname,
                middlename, displayname, telegram_id, start,
                set_type_id, set_count, board, hydro FROM wake""")
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
            """SELECT
                id, firstname, lastname,
                middlename, displayname, telegram_id, start,
                set_type_id, set_count, board, hydro FROM wake
                WHERE id = ?""", [id]))

        if len(rows) == 0:
            return None

        row = rows[0]
        user = User(row[1])
        user.lastname = row[2]
        user.middlename = row[3]
        user.displayname = row[4]
        user.telegram_id = row[5]
        start = datetime.fromtimestamp(row[6])

        return Wake(
            id=row[0], user=user,
            start_date=start.date(), start_time=start.time(),
            set_type_id=row[7], set_count=row[8],
            board=row[9], hydro=row[10])

    def append_data(self, reserve: Wake) -> Wake:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        cursor = self.__connection.cursor()
        cursor.execute("""
            INSERT INTO wake(telegram_id, firstname, lastname,
                middlename, displayname,
                start, set_type_id, set_count, board, hydro)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reserve.user.telegram_id,
                reserve.user.firstname,
                reserve.user.lastname,
                reserve.user.middlename,
                reserve.user.displayname,
                reserve.start.timestamp(),
                reserve.set_type.set_id,
                reserve.set_count,
                reserve.board,
                reserve.hydro
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
            """UPDATE wake SET
                firstname = ?, lastname = ?,
                middlename = ?, displayname = ?, telegram_id = ?, start = ?,
                set_type_id = ?, set_count = ?, board = ?, hydro = ?
                WHERE id = ?
           """, (
                reserve.user.firstname,
                reserve.user.lastname,
                reserve.user.middlename,
                reserve.user.displayname,
                reserve.user.telegram_id,
                reserve.start.timestamp(),
                reserve.set_type.set_id,
                reserve.set_count,
                reserve.board,
                reserve.hydro,
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
            """DELETE FROM wake
                WHERE id = ?
           """, [id])
        self.__connection.commit()

    def create_table(self):
        cursor = self.__connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wake(
                id integer PRIMARY KEY AUTOINCREMENT,
                telegram_id integer,
                firstname text,
                lastname text,
                middlename text,
                displayname text,
                start TIMESTAMP,
                set_type_id text,
                set_count integer,
                board integer, hydro integer)""")

        self.connection.commit()
