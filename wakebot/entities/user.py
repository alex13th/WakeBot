# -*- coding: utf-8 -*-

class User:
    """
    Класс модели пользователя
    """

    def __init__(self,
                 firstname, lastname=None, middlename=None, displayname=None,
                 phone_number=None, telegram_id=None, user_id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self._displayname = displayname
        self.phone_number = phone_number
        self.telegram_id = telegram_id
        self.user_id = user_id

    @property
    def displayname(self):
        """ Отображаемое имя """
        if self._displayname:
            return self._displayname

        result = self.lastname or ""
        result += " " + self.firstname + " "
        result += self.middlename or ""

        return result.strip()

    @displayname.setter
    def displayname(self, value):
        """ Отображаемое имя """
        self._displayname = value

    def __str__(self):
        """ Строковое представление """
        return self.displayname
