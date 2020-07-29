# -*- coding: utf-8 -*-
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from wakebot.adapters.state import StateManager


class StatedProcessor:
    """Base a base stated message processor class

    Attributes:
        strings:
            A locale strings class
        state_manager:
            A state manager class instance
    """
    def __init__(self,
                 dispatcher: Dispatcher,
                 state_manager: StateManager,
                 state_type="*",
                 parse_mode=ParseMode.MARKDOWN):
        """Initialize a class instance

        Args:
            dispatcher:
                A telegram bot dispatcher instance instance.
            state_manager:
                A state manager class instance
            state_type:
                Optional, A default state type.
                Default value: "*" (all state types)
            parse_mode:
                Optional. A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
        """
        self.__dispatcher = dispatcher
        self.__state_manager = state_manager
        self.state_type = state_type
        self.parse_mode = parse_mode

        self.callback_query_handlers = []

    @property
    def state_manager(self):
        return self.__state_manager

    def get_callback_query_filter(self, state, state_type):
        def callback_query_filter(callback_query):
            return self.check_filter(callback_query,
                                     state_type=state_type, state=state)
        return callback_query_filter

    def register_callback_query_handler(self, handler, state, state_type=None):
        state_type = state_type or self.state_type
        callback_filter = self.get_callback_query_filter(state_type=state_type,
                                                         state=state)
        self.__dispatcher.register_callback_query_handler(handler,
                                                          callback_filter)

    def check_filter(self, callback_query, state_type="*", state="*"):
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
        if state_type == "*" and state == "*":
            return True
        self.update_state(callback_query.message)
        current_state_type = self.__state_manager.state_type
        current_state = self.__state_manager.state

        result = (state_type == current_state_type
                  and state == current_state)
        result = (result or
                  (state_type == "*" and state == current_state))
        result = (result or
                  (state_type == current_state_type and state == "*"))

        return result

    def update_state(self, message):
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
        chat_id = message.chat.id
        user_id = message.from_user.id
        message_id = message.message_id
        self.__state_manager.get_state(chat_id, user_id, message_id)
