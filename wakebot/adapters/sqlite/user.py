from sqlite3 import Connection
from typing import Union
from ..data import UserDataAdapter
from ...entities.user import User


class SqliteUserAdapter(UserDataAdapter):
    """Wakeboard SQLite data adapter class

    Attributes:
        connection:
            A SQLite connection instance.
    """

    def __init__(self, connection: Connection, table_name="users"):
        self.__connection = connection
        self.__table_name = table_name
        self.create_table()

    @property
    def connection(self):
        return self.__connection

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
                    is_admin integer)""")

        self.connection.commit()
        cursor.close()

    def get_data(self) -> iter:
        """Get a full set of data from storage

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, phone_number, is_admin"""
            f"  FROM {self.__table_name}")
        for row in cursor:
            yield User(
                user_id=row[0],
                firstname=row[1],
                lastname=row[2],
                middlename=row[3],
                displayname=row[4],
                telegram_id=row[5],
                phone_number=row[6],
                is_admin=bool(row[7])
            )
        cursor.close()

    def get_data_by_keys(self, id: int) -> Union[User, None]:
        """Get a set of data from storage by a keys

        Args:
            id:
                An identifier of user

        Returns:
            A object of given data
        """
        cursor = self.__connection.cursor()
        rows = list(cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, phone_number, is_admin"""
            f"  FROM {self.__table_name} WHERE id = ?", [id]))

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
            phone_number=row[6],
            is_admin=bool(row[7])
        )

    def get_user_by_telegram_id(self, telegram_id: int) -> Union[User, None]:
        """Get a user from storage by telegram_id

        Args:
            telegram_id:
                An telegram identifier of user

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        rows = list(cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, phone_number, is_admin"""
            f"  FROM {self.__table_name} WHERE telegram_id = ?",
            [telegram_id]))

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
            phone_number=row[6],
            is_admin=bool(row[7])
        )

    def append_data(self, user: User) -> User:
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        cursor = self.__connection.cursor()
        cursor.execute(
            f"  INSERT INTO {self.__table_name} ("
            """     telegram_id, firstname, lastname, middlename,
                    displayname, phone_number, is_admin)
                VALUES(?, ?, ?, ?, ?, ?, ?)""", (
                user.telegram_id,
                user.firstname,
                user.lastname,
                user.middlename,
                user.displayname,
                user.phone_number,
                user.is_admin)
        )
        self.__connection.commit()

        result = user.__deepcopy__()
        result.user_id = cursor.lastrowid
        cursor.close()

        return result

    def update_data(self, user: User):
        """Append new data to storage

        Args:
            reserve:
                An instance of entity wake class.
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            f"  UPDATE {self.__table_name} SET"
            """     firstname = ?, lastname = ?, middlename = ?, displayname = ?,
                    phone_number = ?, telegram_id = ?, is_admin = ?
                WHERE id = ?""", (
                user.firstname,
                user.lastname,
                user.middlename,
                user.displayname,
                user.phone_number,
                user.telegram_id,
                user.is_admin,
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
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            f"DELETE FROM {self.__table_name} WHERE id = ?", [id])
        self.__connection.commit()

    def get_admins(self) -> iter:
        """Get administrators list from storage

        Returns:
            A iterator object of given data
        """
        cursor = self.__connection.cursor()
        cursor = cursor.execute(
            """ SELECT id, firstname, lastname, middlename, displayname,
                    telegram_id, phone_number, is_admin"""
            f"  FROM {self.__table_name} WHERE is_admin")

        for row in cursor:
            yield User(
                user_id=row[0],
                firstname=row[1],
                lastname=row[2],
                middlename=row[3],
                displayname=row[4],
                telegram_id=row[5],
                phone_number=row[6],
                is_admin=bool(row[7])
            )
        cursor.close()
