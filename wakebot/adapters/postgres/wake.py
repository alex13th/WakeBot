from datetime import datetime
from typing import Union
from ..data import ReserveDataAdapter
from ...entities.wake import Wake
from ...entities.user import User


class PostgressWakeAdapter(ReserveDataAdapter):
    """Wakeboard SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """

    def __init__(self, connection, table_name="wake_reserves"):
        self.__connection = connection
        self.__table_name = table_name
        self.create_table()

    @property
    def connection(self):
        return self.__connection

    def create_table(self):

        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.__table_name}"
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
                    board integer, hydro integer, count integer)""")

        self.__connection.commit()

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                    id, firstname, lastname,
                    middlename, displayname, telegram_id, start_time,
                    set_type_id, set_count, board, hydro """
                f" FROM {self.__table_name}")
            for row in cursor:
                user = User(row[1])
                user.lastname = row[2]
                user.middlename = row[3]
                user.displayname = row[4]
                user.telegram_id = row[5]
                start = row[6]

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
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """ SELECT id, firstname, lastname, middlename, displayname,
                        telegram_id, start_time, set_type_id, set_count,
                        board, hydro"""
                f"  FROM {self.__table_name}"
                """ WHERE start_time >= %s
                    ORDER BY start_time""", [datetime.today()])

            for row in cursor:
                user = User(row[1])
                user.lastname = row[2]
                user.middlename = row[3]
                user.displayname = row[4]
                user.telegram_id = row[5]
                start = row[6]

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
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """ SELECT id, firstname, lastname, middlename, displayname,
                        telegram_id, phone_number, start_time, set_type_id,
                        set_count, board, hydro"""
                f"  FROM {self.__table_name} WHERE id = %s", [id])

            rows = list(cursor)
            if len(rows) == 0:
                return None

            row = rows[0]
            user = User(row[1])
            user.lastname = row[2]
            user.middlename = row[3]
            user.displayname = row[4]
            user.telegram_id = row[5]
            user.phone_number = row[6]
            start = row[7]

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
        start_ts = reserve.start
        end_ts = reserve.end

        with self.__connection.cursor() as cursor:
            cursor.execute(
                """ SELECT id, firstname, lastname, middlename, displayname,
                        telegram_id, phone_number, start_time, end_time,
                        set_type_id, set_count, board, hydro, count"""
                f"  FROM {self.__table_name}"
                """ WHERE (%s = start_time)
                        or (%s < start_time and %s > start_time)
                        or (%s > start_time and %s < end_time)
                    ORDER BY start_time""",
                (start_ts, start_ts, end_ts, start_ts, start_ts))

            for row in cursor:
                user = User(row[1])
                user.lastname = row[2]
                user.middlename = row[3]
                user.displayname = row[4]
                user.telegram_id = row[5]
                user.phone_number = row[6]
                start = row[7]
                start_date = start.date() if start else None
                start_time = start.time() if start else None

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
        start_ts = reserve.start
        end_ts = reserve.end

        with self.__connection.cursor() as cursor:
            cursor.execute(
                "   SELECT SUM(count) AS concurrent_count"
                f"  FROM {self.__table_name}"
                """ WHERE (%s = start_time)
                        or (%s < start_time and %s > start_time)
                        or (%s > start_time and %s < end_time)""",
                (start_ts, start_ts, end_ts, start_ts, start_ts))

            if cursor:
                row = list(cursor)
            else:
                return 0

            return row[0][0] if row[0][0] else 0

    def append_data(self, reserve: Wake) -> Wake:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"  INSERT INTO {self.__table_name} ("
                """     telegram_id, firstname, lastname,
                        middlename, displayname, phone_number,
                        start_time, end_time, set_type_id, set_count,
                        board, hydro, count)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    reserve.user.telegram_id,
                    reserve.user.firstname,
                    reserve.user.lastname,
                    reserve.user.middlename,
                    reserve.user.displayname,
                    reserve.user.phone_number,
                    reserve.start,
                    reserve.end,
                    reserve.set_type.set_id,
                    reserve.set_count,
                    reserve.board,
                    reserve.hydro,
                    reserve.count
                ))

            result = reserve.__deepcopy__()
            result.id = cursor.fetchone()[0]

            self.__connection.commit()

            return result

    def update_data(self, reserve: Wake):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"  UPDATE {self.__table_name} SET"
                """     firstname = %s, lastname = %s, middlename = %s,
                        displayname = %s, phone_number = %s, telegram_id = %s,
                        start_time = %s, end_time = %s, set_type_id = %s,
                        set_count = %s, board = %s, hydro = %s, count = %s"""
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
                    reserve.board,
                    reserve.hydro,
                    reserve.count,
                    reserve.id))
            self.__connection.commit()

    def remove_data_by_keys(self, id: int):
        """Remove data from storage by a keys

        Args:
            id:
                An identifier of wake reservation

        Returns:
            A iterator object of given data
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self.__table_name} WHERE id = %s", [id])
            self.__connection.commit()
