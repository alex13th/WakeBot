# -*- coding: utf-8 -*-
import unittest
from mocks.aiogram import Dispatcher
from aiogram.types import Chat, User
from aiogram.types import Contact, CallbackQuery, Message
from wakebot.chatprovider import ChatProvider
from wakebot.adapters.data import MemoryDataAdapter


class ChatProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.chat = Chat()
        self.chat.id = 101

        self.user = User()
        self.user.id = 111

        self.command_start_message = Message()
        self.command_start_message.text = "/start"
        self.command_start_message.chat = self.chat
        self.command_start_message.from_user = self.user

        self.command_reserve_message = Message()
        self.command_reserve_message.text = "/reserve"
        self.command_reserve_message.chat = self.chat
        self.command_reserve_message.from_user = self.user
        self.command_reserve_message.message_id = 121

        self.dispatcher = Dispatcher()
        self.data_adapter = MemoryDataAdapter()
        self.provider = ChatProvider(self.dispatcher, self.data_adapter)

    def test_create_object(self):
        """ ChatProvider creation test """
        provider = self.provider

        self.assertEqual(provider._dispatcher, self.dispatcher)
        self.assertEqual(provider._data_adapter, self.data_adapter)

    def test_register_callback_query_handler(self):
        """ Registration callbacky_quer handlers test """
        provider = self.provider
        callback_query1 = CallbackQuery()

        provider.register_callback_query_handler(self.default_callback, [""])
        provider.register_callback_query_handler(self.reserve_callback1,
                                                 ["reserve"], "main")
        provider.register_callback_query_handler(self.reserve_callback2,
                                                 ["reserve"], "book")

        self.assertEqual(len(provider.callback_query_handlers), 2)
        self.assertEqual(len(provider.callback_query_handlers[""]), 1)
        self.assertEqual(provider.callback_query_handlers[""][""](
            callback_query1), "default")
        self.assertEqual(len(provider.callback_query_handlers["reserve"]), 2)
        self.assertEqual(provider.callback_query_handlers["reserve"]["main"](
            callback_query1), "reserve1")
        self.assertEqual(provider.callback_query_handlers["reserve"]["book"](
            callback_query1), "reserve2")

    def test_register_command_handlers(self):
        """ Registration command handlers test """
        provider = self.provider

        provider.register_command_handler(self.default_callback, ["start",
                                                                  "help"])
        provider.register_command_handler(self.reserve_callback1, ["book"],
                                          ["reserve"])

        self.assertEqual(len(provider.command_handlers), 2)
        self.assertEqual(len(provider.command_handlers[""]), 2)
        self.assertEqual(provider.command_handlers[""]["start"](), "default")
        self.assertEqual(provider.command_handlers[""]["help"](), "default")
        self.assertEqual(len(provider.command_handlers["reserve"]), 1)
        self.assertEqual(provider.command_handlers["reserve"]["book"](),
                         "reserve1")

    def test_register_contact_handler(self):
        """ Registration callback_quer handlers test """
        provider = self.provider

        provider.register_contact_handler(self.default_callback)
        provider.register_contact_handler(self.reserve_callback1,
                                          ["reserve", "contact"])
        provider.register_contact_handler(self.reserve_callback2,
                                          ["main"])

        self.assertEqual(len(provider.contact_handlers), 4)
        self.assertEqual(provider.contact_handlers[""](), "default")
        self.assertEqual(provider.contact_handlers["reserve"](),
                         "reserve1")
        self.assertEqual(provider.contact_handlers["contact"](),
                         "reserve1")
        self.assertEqual(provider.contact_handlers["main"](),
                         "reserve2")

    def test_register_message_handler(self):
        """ Registration callback_quer handlers test """
        provider = self.provider

        provider.register_message_handler(self.default_callback)
        provider.register_message_handler(self.reserve_callback1,
                                          ["reserve", "contact"])
        provider.register_message_handler(self.reserve_callback2,
                                          ["main"])

        self.assertEqual(len(provider.message_handlers), 4)
        self.assertEqual(provider.message_handlers[""](), "default")
        self.assertEqual(provider.message_handlers["reserve"](),
                         "reserve1")
        self.assertEqual(provider.message_handlers["contact"](),
                         "reserve1")
        self.assertEqual(provider.message_handlers["main"](),
                         "reserve2")

    def test_proceed_callback_query(self):
        """ Proceed callback_query handlers test """
        provider = self.provider
        callback_query1 = CallbackQuery()
        callback_query1.message = self.command_reserve_message

        provider.register_command_handler(self.reserve_command_for_callback,
                                          ["reserve"])
        provider.register_callback_query_handler(self.reserve_callback1,
                                                 ["reserve"], "main")

        provider.proceed_command(self.command_reserve_message)
        provider.proceed_callback_query(callback_query1)

        self.assertEqual(self.callback_result, "reserve-callback1")

    def test_proceed_command(self):
        """ Proceed command handlers test """
        provider = self.provider

        provider.register_command_handler(self.default_command, ["start",
                                                                 "help"])
        provider.register_command_handler(self.reserve_command, ["reserve"])
        provider.register_command_handler(self.reserve_command_next,
                                          ["reserve"], ["reserve"])

        provider.proceed_command(self.command_start_message)
        self.assertEqual(self.command_result, "default-command: start")

        provider.proceed_command(self.command_reserve_message)
        self.assertEqual(self.command_result, "reserve-command: reserve")
        self.assertEqual(provider.get_state_manager(101, 111).state_type,
                         "reserve")
        self.assertEqual(provider.get_state_manager(101, 111).state,
                         "main")

        provider.proceed_command(self.command_reserve_message)
        self.assertEqual(self.command_result, "reserve-command-next: reserve")
        self.assertEqual(provider.get_state_manager(101, 111).state_type,
                         "reserve")
        self.assertEqual(provider.get_state_manager(101, 111).state,
                         "next")

        # Unregistered command
        self.command_reserve_message.text = "/unregistered"

    def test_proceed_contact(self):
        """ Proceed callback_query handlers test """
        provider = self.provider
        contact = Contact()
        self.command_reserve_message.contact = contact

        provider.register_command_handler(self.reserve_command, ["reserve"])
        provider.register_contact_handler(self.reserve_contact, ["reserve"])

        provider.proceed_command(self.command_reserve_message)
        provider.proceed_contact(self.command_reserve_message)

        self.assertEqual(self.contact_result, "reserve-contact1")

    def test_proceed_message(self):
        """ Proceed callback_query handlers test """
        provider = self.provider
        message = Message()
        message.chat = self.chat
        message.from_user = self.user

        provider.register_command_handler(self.reserve_command, ["reserve"])
        provider.register_message_handler(self.reserve_message, ["reserve"])

        provider.proceed_command(self.command_reserve_message)
        provider.proceed_message(message)

        self.assertEqual(self.message_result, "reserve-message1")

    def default_callback(self, callback_query=None):
        self.callback_result = "default-callback"
        return "default"

    def reserve_callback1(self, callback_query=None):
        self.callback_result = "reserve-callback1"
        return "reserve1"

    def reserve_callback2(self, callback_query=None):
        self.callback_result = "reserve-callback2"
        return "reserve2"

    def default_command(self, command, message):
        self.command_result = "default-command: "
        self.command_result += command
        return "default"

    def reserve_command(self, command, message):
        self.command_result = "reserve-command: "
        self.command_result += command
        chat_id = message.chat.id
        user_id = message.from_user.id
        sm = self.provider.get_state_manager(chat_id, user_id)
        sm.set_state("main", "reserve")
        return "default"

    def reserve_command_next(self, command, message):
        self.command_result = "reserve-command-next: "
        self.command_result += command
        chat_id = message.chat.id
        user_id = message.from_user.id
        sm = self.provider.get_state_manager(chat_id, user_id)
        sm.set_state("next")
        return "default"

    def reserve_command_for_callback(self, command, message):
        self.command_result = "reserve-command-for-callback: "
        self.command_result += command
        chat_id = message.chat.id
        user_id = message.from_user.id
        message_id = message.message_id
        sm = self.provider.get_state_manager(chat_id, user_id, message_id)
        sm.set_state("main", "reserve")
        return "default"

    def reserve_contact(self, message):
        self.contact_result = "reserve-contact1"

    def reserve_message(self, message):
        self.message_result = "reserve-message1"


try:
    unittest.main()
except SystemExit:
    pass
