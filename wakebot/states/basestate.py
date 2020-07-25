# -*- coding: utf-8 -*-

class BaseState:

    def __init__(self, dataAdapter, chat_id, message_id, state_type, user,
                 status="started", state_stage="start", state_id=None):
        pass

    @property
    def state_id(self):
        """Идентификатор состояния"""
        pass

    @property
    def chat_id(self):
        """Идентификатор чата с пользователем"""
        pass

    @property
    def message_id(self):
        """Идентификатор сообщения, которым инициировано данное состояние"""
        pass

    @property
    def state_type(self):
        """Тип состояния (определяет выбор процессора обработки сообщений)"""
        pass

    @property
    def user(self):
        """Информация о пользователе"""
        pass

    @property
    def state_stage(self):
        """Состояние резервирования (этап)"""
        pass

    @property
    def status(self):
        """Степень завершенности (started/progress/completed)"""
        pass

    def get_message_text(self):
        pass

    def get_message_keyboard(self):
        pass
