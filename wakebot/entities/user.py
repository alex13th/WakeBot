# -*- coding: utf-8 -*-

class User:
    """
    Класс модели пользователя
    """

    def __init__(self, 
                 firstname, lastname=None, middlename=None, displayname=None,
                 phone_number=None, telegram_id=None, user_id=None):
        pass

    @property
    def user_id(self):
        """ Идентификатор пользователя """
        pass

    @property
    def telegram_id(self):
        """ Идентификатор в Телеграм """
        pass

    @property
    def firstname(self):
        """ Имя """
        pass

    @property
    def lastname(self):
        """ Фамилия """
        pass

    @property
    def middlename(self):
        """ Отчество """
        pass

    @property
    def displayname(self):
        """ Отображаемое имя """
        pass

    @property
    def phone_number(self):
        """ Номер телефона """
        pass

    def __str__(self):
        """ Строковое представление """
        return ""
