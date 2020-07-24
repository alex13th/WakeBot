# -*- coding: utf-8 -*-

class ChatProvider:
    """ Класс основного процессора бота """

    def __init__(self, dataAdapter, token):
        """ Параметры:
        dataAdapter - объект обеспечивающий доступ к БД
        token - токен телеграм бота
        """
        pass

    @property
    def bot(self):
        """ Объект telebot """
        pass

    @property
    def state(self):
        """ Объект состояния чата с пользователем """
        pass

    def proceed_text(self, message):
        """ Метод обработки поступающих текстовых сообщений """
        pass

    def proceed_command(self, message):
        """ Метод обработки команд """
        pass

    def proceed_callback_query(self, message):
        """ Метод обработки обратных вызовов """
        pass

    def load_state(self):
        """ Метод загрузки состояния чата из БД """
        pass

    def save_state(self):
        """ Метод сохранения состояния чата из БД """
        pass

    def create_processor(self, message):
        """ Метод создания процессора обработки сообщений """
        pass
