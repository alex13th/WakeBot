from typing import Union
from ..data import UserDataAdapter
from ...entities.user import User


class PostgresUserAdapter(UserDataAdapter):
    """Wakeboard SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """

    def __init__(self, connection):
        self.__connection = connection
        self.create_table()

    @property
    def connection(self):
        return self.__connection

    def create_table(self):
        with self.__connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    telegram_id integer,
                    firstname varchar(20),
                    lastname varchar(20),
                    middlename varchar(20),
                    displayname varchar(60),
                    phone_number varchar(20))""")

            self.connection.commit()

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                    id, firstname, lastname,
                    middlename, displayname, telegram_id, phone_number
                    FROM users""")
            for row in cursor:
                yield User(
                    user_id=row[0],
                    firstname=row[1],
                    lastname=row[2],
                    middlename=row[3],
                    displayname=row[4],
                    telegram_id=row[5],
                    phone_number=row[6]
                )

    def get_data_by_keys(self, id: int) -> Union[User, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of user

        Returns:
            A object of given data
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                    id, firstname, lastname,
                    middlename, displayname, telegram_id, phone_number
                    FROM users
                    WHERE id = %s""", [id])

            rows = list(cursor)
            if len(rows) == 0:
                return None

            row = rows[0]
            cursor.close()
            return User(
                user_id=row[0],
                firstname=row[1],
                lastname=row[2],
                middlename=row[3],
                displayname=row[4],
                telegram_id=row[5],
                phone_number=row[6]
            )

    def get_user_by_telegram_id(self, telegram_id: int) -> Union[User, None]:
        """Get a user from storage by telegram_id

        Args:
            telegram_id:
                An telegram identifier of user

        Returns:
            A iterator object of given data
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                    id, firstname, lastname,
                    middlename, displayname, telegram_id, phone_number
                    FROM users
                    WHERE telegram_id = %s""", [telegram_id])

            rows = list(cursor)
            if len(rows) == 0:
                return None

            row = rows[0]
            cursor.close()
            return User(
                user_id=row[0],
                firstname=row[1],
                lastname=row[2],
                middlename=row[3],
                displayname=row[4],
                telegram_id=row[5],
                phone_number=row[6]
            )

    def append_data(self, user: User) -> User:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users(telegram_id, firstname, lastname,
                    middlename, displayname, phone_number)
                    VALUES(%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    user.telegram_id,
                    user.firstname,
                    user.lastname,
                    user.middlename,
                    user.displayname,
                    user.phone_number)
            )

            result = user.__deepcopy__()
            result.user_id = cursor.fetchone()[0]

            self.__connection.commit()

            return result

    def update_data(self, user: User):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """UPDATE users SET
                    firstname = %s, lastname = %s, middlename = %s,
                    displayname = %s, phone_number = %s, telegram_id = %s
                    WHERE id = %s
            """, (
                    user.firstname,
                    user.lastname,
                    user.middlename,
                    user.displayname,
                    user.phone_number,
                    user.telegram_id,
                    user.user_id
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
        with self.__connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM users
                    WHERE id = %s
            """, [id])
            self.__connection.commit()
