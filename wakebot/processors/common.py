from typing import Union, Callable
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode, Message, CallbackQuery
from wakebot.adapters.state import StateManager


class StatedProcessor:
    """Base a base stated message processor class
    Attributes:
        dispatcher:
            An aiogram.Dispatcher class instance
        state_manager:
            A state manager class instance
            state_type:
                A default state type.
                Default value: "*" (all state types)
            parse_mode:
                A parse mode of telegram messages (ParseMode).
                Default value: aiogram.types.ParseMode.MARKDOWN
    """

    __dispatcher: Dispatcher
    __state_manager: StateManager
    state_type: Union[str, int, None]
    parse_mode = ParseMode.MARKDOWN

    def __init__(self,
                 dispatcher: Dispatcher,
                 state_manager: StateManager,
                 state_type: Union[str, int, None] = "*",
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
    def state_manager(self) -> StateManager:
        return self.__state_manager

    @property
    def dispatcher(self) -> Dispatcher:
        return self.__dispatcher

    def get_callback_query_filter(self,
                                  state: Union[str, int, None],
                                  state_type: Union[str, int, None]):
        """Generate a function to apply a state and state_type filter
           to CallbackQuery handler.

        Args:
            state:
                A string state filter:
                    "*" - any state
                    "" - state has no value filter
            state_type:
                A string state type filter:
                    "*" - any state type
                    "" - state type has no value filter
        """
        def callback_query_filter(callback_query: CallbackQuery):
            return self.check_filter(
                message=callback_query.message, state_type=state_type,
                state=state, message_state=True)
        return callback_query_filter

    def get_message_filter(self,
                           state: Union[str, int, None],
                           state_type: Union[str, int, None]):
        """Generate a function to apply a state and state_type filter
           to CallbackQuery handler.

        Args:
            state:
                A string state filter:
                    "*" - any state
                    "" - state has no value filter
            state_type:
                A string state type filter:
                    "*" - any state type
                    "" - state type has no value filter
        """
        def message_filter(message):
            return self.check_filter(
                message, state_type=state_type, state=state,
                message_state=False)
        return message_filter

    def register_callback_query_handler(
                            self,
                            handler: Callable[[CallbackQuery], None],
                            state: Union[str, int, None],
                            state_type: Union[str, int, None] = None):
        """Register CallbackQuery handler with state and state_type filters

        Args:
            handler:
                A CallbackQuery handler function - f(callback_query).
            state:
                A string state filter:
                    "*" - any state
                    "" - state has no value filter
            state_type:
                A string state type filter:
                    "*" - any state type
                    "" - state type has no value filter
        """
        state_type = state_type or self.state_type
        callback_filter = self.get_callback_query_filter(state_type=state_type,
                                                         state=state)
        self.__dispatcher.register_callback_query_handler(handler,
                                                          callback_filter)

    def register_message_handler(
                            self,
                            handler: Callable[[Message], None],
                            state: Union[str, int, None],
                            state_type: Union[str, int, None] = None):
        """Register Message handler with state and state_type filters

        Args:
            handler:
                A Message handler function - f(message).
            state:
                A string state filter:
                    "*" - any state
                    "" - state has no value filter
            state_type:
                A string state type filter:
                    "*" - any state type
                    "" - state type has no value filter
        """
        state_type = state_type or self.state_type
        message_filter = self.get_message_filter(state_type=state_type,
                                                 state=state)
        self.__dispatcher.register_message_handler(handler, message_filter)

    def check_filter(self, message: Message,
                     state_type: Union[str, int, None] = "*",
                     state: Union[str, int, None] = "*",
                     message_state: bool = True):
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
        self.update_state(message, message_state=message_state)
        current_state_type = self.__state_manager.state_type
        current_state = self.__state_manager.state

        result = (state_type == current_state_type
                  and state == current_state)
        result = (result or
                  (state_type == "*" and state == current_state))
        result = (result or
                  (state_type == current_state_type and state == "*"))

        return result

    def update_state(self, message: Message, message_state: bool = True):
        """Update StateManager for message

        Args:
            message:
                A message to check matching
            message_state:
                A boolean indicates to need use message_id for define state
        """
        chat_id = message.chat.id
        user_id = message.from_user.id
        message_id = message.message_id if message_state else None
        self.__state_manager.get_state(chat_id, user_id, message_id)
