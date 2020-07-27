
# -*- coding: utf-8 -*-
from wakebot.adapters.data import BaseDataAdapter


class StateManager:
    """Manager of current state

    Attributes:
        data_adapter:
            A BaseDataAdapter object of a state storage
        state_id:
            A calculated state idenfifier
        state_type:
            A current state type
        state:
            A current state
    """

    def __init__(self, data_adapter: BaseDataAdapter,
                 chat_id=None, user_id=None, message_id=None):
        """Initialize StateManager object

        Args:
            data_adapter:
                A BaseDataAdapter object of a state storage
            chat_id:
                An int or str a telegramm chat Id
            user_id:
            message_id:
                Optinal. An int or str a telegramm message Id
        """
        self.__data_adapter = data_adapter
        self.__state_type = ""
        self.__state = ""
        self.__data = None

        self.get_state(chat_id, user_id, message_id)

    @property
    def data_adapter(self):
        return self.__data_adapter

    @property
    def state_id(self):
        result = str(self.__chat_id)
        result += f"-{self.__user_id}" if self.__user_id else ""
        result += f"-{self.__message_id}" if self.__message_id else ""

        return result

    @property
    def state_type(self):
        return self.__state_type

    @property
    def state(self):
        return self.__state

    def get_state(self, chat_id, user_id, message_id=None):
        """Get current state from data adapter """
        self.__chat_id = chat_id
        self.__user_id = user_id
        self.__message_id = message_id

        if chat_id and user_id:
            state_data = self.__data_adapter.get_data_by_keys(
                key=self.state_id)
            if state_data:
                self.__state_type = state_data["state_type"]
                self.__state = state_data["state"]

    def set_state(self, state=None, state_type=None,
                  message_id=None, data=None):
        """Set current state to data adapter

            Args:
                state:
                    Optional. A string or integer state
                state_type:
                    Optional. A string type of state
                message_id:
                    Optional. A string type of state
                data:
                    Optional. A dictionary that contain a state data
        """
        self.__state = state if state else self.__state
        self.__state_type = state_type if state_type else self.__state_type
        self.__message_id = message_id if message_id else self.__message_id
        self.__data = data if data else self.__data

        state_data = {}
        state_data["state"] = self.__state
        state_data["state_type"] = self.__state_type

        if not (self.__data is None):
            state_data["data"] = self.__data

        self.data_adapter.update_data(self.state_id, state_data)

    def finish(self):
        """Remove current state"""
        pass


class StateProvider:

    def __init__(self, data_adapter: BaseDataAdapter):
        self.__data_adapter = data_adapter
        self.__state_manager = StateManager(data_adapter)
        self.__message_handlers = []
        self.__callback_handlers = []

    def command_state(self, state_type="*", state="*"):
        def decorator(callback):
            async def command_function(message):
                if state_type == "*" and state == "*":
                    await callback(message, self.__state_manager)
                    return

                chat_id = message.chat.id
                user_id = message.from_user.id
                message_id = message.message_id

                self.__state_manager.get_state(chat_id, user_id, message_id)
                current_state_type = self.__state_manager.state_type
                current_state = self.__state_manager.state

                if state_type == current_state_type and state == current_state:
                    await callback(message, self.__state_manager)
                elif state_type == "*" and state == current_state:
                    await callback(message, self.__state_manager)
                elif state_type == current_state_type and state == "*":
                    await callback(message, self.__state_manager)

            return command_function

        return decorator

    def callback_query_state(self, callback_query):
        pass
