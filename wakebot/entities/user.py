import re

from typing import Optional


class User:
    """User data class

    Attributes:
        firstname:
            A user firstname
        lastname:
            A user lastname
        middlename:
            A user middlename
        displayname:
            A string value is joined by firstname, middlename, lastname.
            Also can be setted manually.
        phone_number:
            A string present usere phone number
        telegram_id:
            A string/integer telegram user id
        user_id:
            An integer internal user id.
        is_admin:
            A boolean flag of user admin role.
    """

    __slots__ = ["firstname", "lastname", "middlename", "_displayname",
                 "_phone_number", "telegram_id", "user_id", "is_admin"]
    phone_regex = "^\\+[7]\\s?[-\\(]?\\d{3}\\)?[- ]?\\d{3}-?\\d{2}-?\\d{2}$"

    def __init__(self,
                 firstname: str,
                 lastname: Optional[str] = None,
                 middlename: Optional[str] = None,
                 displayname: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 telegram_id: Optional[int] = None,
                 user_id: Optional[int] = None,
                 is_admin: bool = False):
        """User data class

        Args:
            firstname:
                A user firstname
            lastname:
                A user lastname
            middlename:
                A user middlename
            displayname:
                A string value is joined by firstname, middlename, lastname.
                Also can be setted manually.
            phone_number:
                A string present usere phone number
            telegram_id:
                A string/integer telegram user id
            user_id:
                An integer internal user id.
            is_admin:
                A boolean flag of user admin role.
        """
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self._displayname = displayname
        self.phone_number = phone_number
        self.telegram_id = telegram_id
        self.user_id = user_id
        self.is_admin = is_admin

    @property
    def displayname(self) -> str:
        if self._displayname:
            return self._displayname

        result = self.lastname or ""
        result += " " + self.firstname + " "
        result += self.middlename or ""

        return result.strip()

    @displayname.setter
    def displayname(self, value: str):
        self._displayname = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: Optional[str]):
        if (not value) or re.match(self.phone_regex, value):
            self._phone_number = value
        else:
            self._phone_number = value

    def __copy__(self):
        return User(
            self.firstname, self.lastname, self.middlename,
            self._displayname, self.phone_number,
            self.telegram_id, self.user_id, is_admin=self.is_admin)

    def __str__(self) -> str:
        """Provide built-in mapping to string"""
        return self.displayname

    def __eq__(self, other) -> bool:
        """ Compare all attributes exclude user_id """
        if (self.firstname == other.firstname
                and self.lastname == other.lastname
                and self.middlename == other.middlename
                and self.displayname == other.displayname
                and self.phone_number == other.phone_number
                and self.telegram_id == other.telegram_id):
            return True
        else:
            return False

    def __repr__(self) -> str:
        """Provide built-in mapping to represantation string"""
        return (f"User(displayname={self.displayname!r}, "
                f"telegram_id={self.telegram_id!r}, "
                f"phone_number={self.phone_number!r}, "
                f"user_id={self.user_id})")
