# -*- coding: utf-8 -*-

class User:
    """
    Класс модели пользователя
    """

    @property
    def user_id(self):
        """ Идентификатор пользователя """
        pass

    @property
    def telegram_id(self):
        """ Идентификатор в Телеграм """
        pass

    @property
    def first_name(self):
        """ Имя """
        pass

    @property
    def last_name(self):
        """ Фамилия """
        pass

    @property
    def middle_name(self):
        """ Отчество """
        pass

    @property
    def display_name(self):
        """ Отображаемое имя """
        pass

    @property
    def phone_namber(self):
        """ Номер телефона """
        pass

    def __str__(self):
        """ Строковое представление """
        pass
