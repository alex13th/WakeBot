import psycopg2
from datetime import datetime
from typing import Union
from ..data import ReserveDataAdapter
from ...entities import Bathhouse, User


class PostgressBathhouseAdapter(ReserveDataAdapter):
    """Bathhouse PostgreSQL data adapter class

    Attributes:
        connection:
            A PostgreSQL connection instance.
    """
    __connection = None

    def __init__(self, connection=None,
                 db_url: Union[str, None] = None,
                 table_name="bathhouse_reserves"):
        if connection:
            self.__connection = connection
        else:
            self.__db_url = db_url
            self.connect()

        self.__table_name = table_name
        self.create_table()

    @property
    def connection(self):
        return self.__connection

    def connect(self):
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            self.__connection = psycopg2.connect(self.__db_url)

    def create_table(self):
        self.connect()
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
                    count integer,
                    canceled boolean DEFAULT false,
                    cancel_telegram_id integer)""")

        self.__connection.commit()

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                    id, firstname, lastname,
                    middlename, displayname, telegram_id, start_time,
                    set_type_id, set_count, count """
                f" FROM {self.__table_name}")

            self.__connection.commit()

            for row in cursor:
                user = User(row[1])
                user.lastname = row[2]
                user.middlename = row[3]
                user.displayname = row[4]
                user.telegram_id = row[5]
                start = row[6]

                yield Bathhouse(
                    id=row[0], user=user,
                    start_date=start.date(), start_time=start.time(),
                    set_type_id=row[7], set_count=row[8],
                    count=row[9])

    def get_active_reserves(self) -> iter:
        """Get an active Bathhouse reservations from storage

        Returns:
            A iterator object of given data
        """
        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """ SELECT id, firstname, lastname, middlename, displayname,
                        telegram_id, start_time, set_type_id,
                        set_count, count"""
                f"  FROM {self.__table_name}"
                """ WHERE NOT canceled
                        and start_time >= %s
                    ORDER BY start_time""", [datetime.today()])

            self.__connection.commit()

            for row in cursor:
                user = User(row[1])
                user.lastname = row[2]
                user.middlename = row[3]
                user.displayname = row[4]
                user.telegram_id = row[5]
                start = row[6]

                yield Bathhouse(
                    id=row[0], user=user,
                    start_date=start.date(), start_time=start.time(),
                    set_type_id=row[7], set_count=row[8],
                    count=row[9])

    def get_data_by_keys(self, id: int) -> Union[Bathhouse, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of Bathhouse reservation

        Returns:
            A iterator object of given data
        """
        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """ SELECT id, firstname, lastname, middlename, displayname,
                        telegram_id, phone_number, start_time, set_type_id,
                        set_count, count, canceled, cancel_telegram_id
                        """
                f"  FROM {self.__table_name} WHERE id = %s", [id])

            self.__connection.commit()

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

            return Bathhouse(
                id=row[0], user=user,
                start_date=start.date(), start_time=start.time(),
                set_type_id=row[8], set_count=row[9],
                count=row[10], canceled=row[11], cancel_telegram_id=row[12])

    def get_concurrent_reserves(self, reserve: Bathhouse) -> iter:
        """Get an concurrent reservations from storage

        Returns:
            A iterator object of given data
        """
        start_ts = reserve.start
        end_ts = reserve.end

        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """ SELECT id, firstname, lastname, middlename, displayname,
                        telegram_id, phone_number, start_time,
                        set_type_id, set_count, count"""
                f"  FROM {self.__table_name}"
                """ WHERE NOT canceled
                        and ((%s = start_time)
                        or (%s < start_time and %s > start_time)
                        or (%s > start_time and %s < end_time))
                    ORDER BY start_time""",
                (start_ts, start_ts, end_ts, start_ts, start_ts))

            self.__connection.commit()

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

                yield Bathhouse(
                    id=row[0], user=user,
                    start_date=start_date, start_time=start_time,
                    set_type_id=row[8], set_count=row[9],
                    count=row[10])

    def get_concurrent_count(self, reserve: Bathhouse) -> int:
        """Get an concurrent reservations count from storage

        Returns:
            An integer count of concurrent reservations
        """
        start_ts = reserve.start
        end_ts = reserve.end

        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "   SELECT SUM(count) AS concurrent_count"
                f"  FROM {self.__table_name}"
                """ WHERE NOT canceled
                        and ((%s = start_time)
                        or (%s < start_time and %s > start_time)
                        or (%s > start_time and %s < end_time))""",
                (start_ts, start_ts, end_ts, start_ts, start_ts))

            self.__connection.commit()

            if cursor:
                row = list(cursor)
            else:
                return 0

            return row[0][0] if row[0][0] else 0

    def append_data(self, reserve: Bathhouse) -> Bathhouse:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity Bathhouse class.
        """
        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"  INSERT INTO {self.__table_name} ("
                """     telegram_id, firstname, lastname, middlename,
                        displayname, phone_number, start_time, end_time,
                        set_type_id, set_count, count)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    reserve.count
                ))

            result = reserve.__deepcopy__()
            result.id = cursor.fetchone()[0]

            self.__connection.commit()

            return result

    def update_data(self, reserve: Bathhouse):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity Bathhouse class.
        """
        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"  UPDATE {self.__table_name} SET"
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

            self.__connection.commit()

    def remove_data_by_keys(self, id: int):
        """Remove data from storage by a keys

        Args:
            id:
                An identifier of Bathhouse reservation

        Returns:
            A iterator object of given data
        """
        self.connect()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self.__table_name} WHERE id = %s", [id])
            self.__connection.commit()
