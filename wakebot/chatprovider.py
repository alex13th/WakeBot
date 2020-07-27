# -*- coding: utf-8 -*-
from aiogram.dispatcher import Dispatcher
from wakebot.adapters.state import StateManager


class ChatProvider:
    """Proceed incoming messages

    Attributes:
        dispatcher:
            A telegram bot dispatcher.
        data_adapter:
            A BaseDataAdapter object of a state storage.
    """
    def __init__(self, dispatcher: Dispatcher, data_adapter):
        """Initialize ChatProvider object

        Args:
            dispatcher:
                A telegram bot dispatcher.
            data_adapter:
                A BaseDataAdapter object of a state storage.
        """
        self._dispatcher = dispatcher
        self._data_adapter = data_adapter

        # Dictionary:
        #   {"state_type"={"command_name"=handler}}
        # Examples:
        #   {"reserve"={"list"=reserve_list, "contact"=reserve_contact}},
        #    ""={"start"=default_start, "help"=default_help}}

        self.callback_query_handlers = {}
        dispatcher.register_callback_query_handler(self.proceed_callback_query)

        self.command_handlers = {}
        dispatcher.register_message_handler(self.register_command_handler)

        self.contact_handlers = {}

        self.message_handlers = {}

    def register_callback_query_handler(self, handler, state_types=[""],
                                        state=""):
        """Register callback_query handler

        Args:
            handler:
                A callback function to proceed CallbackQuery object.
            state_types:
                A list of a state types applied to handler.
        """
        for state_type in state_types:
            if not self.callback_query_handlers.get(state_type):
                self.callback_query_handlers[state_type] = {}
            self.callback_query_handlers[state_type][state] = handler

    def proceed_callback_query(self, callback_query):
        """Call a callback query handlers applied to current state

        Args:
            callback_query:
                A CallbackQuery object
        """
        state_manager = self.get_current_state_manager(
            callback_query=callback_query)
        state_type = state_manager.state_type
        state = state_manager.state

        try:
            self.callback_query_handlers[state_type][state](callback_query)
        except KeyError:
            pass

    def register_command_handler(self, handler, commands,
                                 state_types=[""]):
        """Register command handler

        Args:
            handler:
                A callback function to proceed a command.
            commands:
                A list of commands applied to handler.
            state_types:
                A list of a state types applied to handler.
        """
        for state_type in state_types:
            if not self.command_handlers.get(state_type):
                self.command_handlers[state_type] = {}
            for command in commands:
                self.command_handlers[state_type][command] = handler

    def proceed_command(self, message):
        """Call a command handlers applied to current state

        Args:
            messsage:
                A Message object
        """
        command = message.get_command(True)
        state_manager = self.get_current_state_manager(message=message)
        state_type = state_manager.state_type

        try:
            self.command_handlers[state_type][command](command, message)
        except KeyError:
            pass

    def register_contact_handler(self, handler, state_types=[""]):
        """Register contact handler

        Args:
            handler:
                A callback function to proceed a contact.
            state_types:
                A list of a state types applied to handler.
        """
        for state_type in state_types:
            if not self.contact_handlers.get(state_type):
                self.contact_handlers[state_type] = {}
            self.contact_handlers[state_type] = handler

    def proceed_contact(self, message):
        """Call a command handlers applied to current state

        Args:
            messsage:
                A Message object
        """
        state_manager = self.get_current_state_manager(message=message)

        try:
            self.contact_handlers[state_manager.state_type](message)
        except KeyError:
            pass

    def register_message_handler(self, handler, state_types=[""]):
        """Register message handler

        Args:
            handler:
                A callback function to proceed a command.
            state_types:
                A list of a state types applied to handler.
        """
        for state_type in state_types:
            if not self.message_handlers.get(state_type):
                self.message_handlers[state_type] = {}
            self.message_handlers[state_type] = handler

    def proceed_message(self, message):
        """Call a message handlers applied to current state

        Args:
            messsage:
                A Message object
        """
        state_manager = self.get_current_state_manager(message=message)

        try:
            self.message_handlers[state_manager.state_type](message)
        except KeyError:
            pass

    def get_state_manager(self, chat_id, user_id,
                          message_id=None) -> StateManager:
        """Return current state manager object

        Returns:
            A StateManager object
        """
        return StateManager(self._data_adapter, chat_id, user_id, message_id)

    def get_current_state_manager(self, message=None, callback_query=None):
        if message:
            chat_id = message.chat.id
            user_id = message.from_user.id
            return self.get_state_manager(chat_id, user_id)

        elif callback_query:
            chat_id = callback_query.message.chat.id
            user_id = callback_query.message.from_user.id
            message_id = callback_query.message.message_id

            return self.get_state_manager(chat_id, user_id, message_id)
