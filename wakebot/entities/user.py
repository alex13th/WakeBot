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

    firstname: str
    lastname: Optional[str]
    middlename: Optional[str]
    _displayname: Optional[str]
    phone_number: Optional[str]
    telegram_id: Optional[int]
    user_id: Optional[int]
    is_admin: Optional[bool]

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
    def displayname(self, value: Optional[str]):
        self._displayname = value

    def __copy__(self):
        return User(
            self.firstname, self.lastname, self.middlename,
            self._displayname, self.phone_number,
            self.telegram_id, self.user_id, is_admin=self.is_admin)

    def __deepcopy__(self):
        return self.__copy__()

    def __str__(self) -> str:
        """Provide built-in mapping to string"""
        return self.displayname
