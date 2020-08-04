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

    @property
    def data(self):
        return self.__data

    def get_state(self, chat_id, user_id, message_id=None):
        """Get current state from data adapter """
        self.__chat_id = chat_id
        self.__user_id = user_id
        self.__message_id = message_id

        if chat_id and user_id:
            state_data: dict = self.__data_adapter.get_data_by_keys(
                key=self.state_id)
            if state_data:
                self.__state_type = state_data["state_type"]
                self.__state = state_data["state"]
                self.__data = state_data.get("data", None)
            else:
                self.__state_type = ""
                self.__state = ""
                self.__data = None

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

        if self.__data:
            state_data["data"] = self.__data

        self.data_adapter.update_data(self.state_id, state_data)

    def set_data(self, data):
        self.__data = data

    def finish(self):
        """Remove current state"""
        self.__data_adapter.remove_data_by_keys(self.state_id)


class StateProvider:
    """Provide state filter

    Attributes:
        data_adapter:
            A data adapter of a state storage
    """
    def __init__(self, data_adapter=None):
        """Initialize StateProvider object

        Args:
            data_adapter:
                Optional. A data adapter object of a state storage
        """
        self.__data_adapter = data_adapter
        self.__state_manager = StateManager(data_adapter)

    @property
    def data_adapter(self):
        return self.__data_adapter

    @data_adapter.setter
    def data_adapter(self, value):
        self.__data_adapter = value
        self.__state_manager = StateManager(value)

    def message_state(self, state_type="*", state="*"):
        """Decorator state type and(or) state filter for message function

            Args:
                state_type:
                    Optional. A string state type filter:
                        "*" - any state type
                        "" - state type has no value filter
                state:
                    Optional. A string state filter:
                        "*" - any state
                        "" - state has no value filter
        """
        def decorator(top_cls, message_handler=None):
            if not message_handler:
                message_handler = top_cls

            async def message_decorator(cls, message=None):
                if message:
                    self.update_state_manager(message)
                    if state_type == "*" and state == "*":
                        await message_handler(cls, message,
                                              self.__state_manager)
                        return

                    if self.check_filter(state_type, state, message):
                        await message_handler(cls, message,
                                              self.__state_manager)
                else:
                    message = cls
                    self.update_state_manager(message)
                    if state_type == "*" and state == "*":
                        await message_handler(message, self.__state_manager)
                        return

                    if self.check_filter(state_type, state, message):
                        await message_handler(message, self.__state_manager)

            return message_decorator
        return decorator

    def callback_query_state(self, state_type="*", state="*"):
        """Set state type and(or) state filter for callback_query function

            Args:
                state_type:
                    Optional. A string state type filter:
                        "*" - any state type
                        "" - state type has no value filter
                state:
                    Optional. A string state filter:
                        "*" - any state
                        "" - state has no value filter
        """
        def decorator(top_cls, callback_query_handler=None):
            if not callback_query_handler:
                callback_query_handler = top_cls

            async def callback_query_decorator(cls, callback_query=None):
                if callback_query_handler:
                    message = callback_query.message

                    self.update_state_manager(message)

                    if state_type == "*" and state == "*":
                        await callback_query_handler(cls, callback_query,
                                                     self.__state_manager)
                        return

                    if self.check_filter(state_type, state, message):
                        await callback_query_handler(cls, callback_query,
                                                     self.__state_manager)
                else:
                    callback_query = cls
                    message = callback_query.message

                    self.update_state_manager(message)

                    if state_type == "*" and state == "*":
                        await callback_query_handler(cls, callback_query,
                                                     self.__state_manager)
                        return

                    if self.check_filter(state_type, state, message):
                        await callback_query_handler(cls, callback_query,
                                                     self.__state_manager)

            return callback_query_decorator
        return decorator

    def check_filter(self, state_type, state, message):
        """Check message is matched filter

            Args:
                state_type:
                    A string state type filter:
                        "*" - any state type
                        "" - state type has no value filter
                state:
                    A string state filter:
                        "*" - any state
                        "" - state has no value filter
                message:
                    A message to check matching
        """
        current_state_type = self.__state_manager.state_type
        current_state = self.__state_manager.state

        result = (state_type == current_state_type
                  and state == current_state)
        result = (result or
                  (state_type == "*" and state == current_state))
        result = (result or
                  (state_type == current_state_type and state == "*"))

        return result

    def update_state_manager(self, message):
        """Update state manager
            Args:
                state_type:
                    A message object to get state
        """
        chat_id = message.chat.id
        user_id = message.from_user.id
        message_id = message.message_id
        self.__state_manager.get_state(chat_id, user_id, message_id)
