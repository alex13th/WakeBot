# -*- coding: utf-8 -*-
from aiogram.dispatcher import Dispatcher


class BaseProcessor:
    """ Базовый класс обработки сообщений
    """

    def __init__(self, dispatcher: Dispatcher, state):
        """
            provider: объект основного процессора бота;
            state: объект состояния чата.
        """
        pass

    @property
    def provided_commands(self):
        """ Кортеж поддерживаемых команд """
        pass

    """
    Методы реализуемые потомками по мере необходимости

    def proceed_text(self, text):
        pass

    def proceed_command(self, command):
        pass

    def proceed_callback_query(self, callback):
        pass

    def proceed_contact(self, proceed_contact):
        pass
    """
