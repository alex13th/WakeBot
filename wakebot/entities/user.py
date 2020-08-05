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
    """

    firstname: str
    lastname: Optional[str]
    middlename: Optional[str]
    _displayname: Optional[str]
    phone_number: Optional[str]
    telegram_id: Optional[int]
    user_id: Optional[int]

    def __init__(self,
                 firstname: str,
                 lastname: Optional[str] = None,
                 middlename: Optional[str] = None,
                 displayname: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 telegram_id: Optional[int] = None,
                 user_id: Optional[int] = None):
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
        """
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self._displayname = displayname
        self.phone_number = phone_number
        self.telegram_id = telegram_id
        self.user_id = user_id

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

    def __str__(self) -> str:
        """Provide built-in mapping to string"""
        return self.displayname
