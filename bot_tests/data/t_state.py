# -*- coding: utf-8 -*-
from ..base_test_case import BaseTestCase

from aiogram.types import Chat, User
from aiogram.types import Message, CallbackQuery
from wakebot.adapters.state import StateManager, StateProvider
from wakebot.adapters.data import MemoryDataAdapter


class StateManagerTestCase(BaseTestCase):
    """StateManager class"""
    def setUp(self):
        self.data_adapter = MemoryDataAdapter()

        state_data = {"state": "main", "state_type": "reserve"}
        self.data_adapter.append_data("101-111-122", state_data)
        self.data_adapter.append_data("101-111-122", state_data)

    async def test_create_object(self):
        state_mgr = StateManager(self.data_adapter, 101, 111)

        passed, alert = self.assert_params(state_mgr.data_adapter,
                                           self.data_adapter)
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state_id, "101-111")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state_type, "")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state, "")
        assert passed, alert

    async def test_create_object_with_message(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 121)

        passed, alert = self.assert_params(state_mgr.state_id, "101-111-121")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state_type, "")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state, "")
        assert passed, alert

    async def test_create_object_with_storied(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 122)

        passed, alert = self.assert_params(state_mgr.state_id, "101-111-122")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state_type, "reserve")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state, "main")
        assert passed, alert

    async def test_change_state(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 122)

        state_mgr.set_state("book")

        passed, alert = self.assert_params(state_mgr.state_id, "101-111-122")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state_type, "reserve")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state, "book")
        assert passed, alert

    async def test_change_state_type(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 122)

        state_mgr.set_state(state_type="reserve1")

        passed, alert = self.assert_params(state_mgr.state_id, "101-111-122")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state_type, "reserve1")
        assert passed, alert
        passed, alert = self.assert_params(state_mgr.state, "main")
        assert passed, alert

    async def test_set_state(self):
        state_mgr = StateManager(self.data_adapter, 101, 111)

        state_mgr.set_state("book2", "reserve2", 122)
        state_data = self.data_adapter.get_data_by_keys("101-111-122")

        passed, alert = self.assert_params(state_data["state_type"],
                                           "reserve2")
        assert passed, alert
        passed, alert = self.assert_params(state_data["state"], "book2")
        assert passed, alert


class StateProviderTestCase(BaseTestCase):
    """StateProvider class"""

    state_provider = StateProvider()

    @state_provider.message_state()
    async def message_default(self, message, state_manager):
        self.result_text = "Default message"

    @state_provider.message_state(state_type="reserve", state="main")
    async def message_reserve_main(self, message, state_manager):
        self.result_text = (f"{message.text}: {state_manager.state_type}" +
                            f" {state_manager.state}")

    @state_provider.callback_query_state(state_type="reserve", state="book")
    async def callback_query_reserve_book(self, callback_query, state_manager):
        self.result_text = (f"Callback: {state_manager.state_type}" +
                            f" {state_manager.state}")

    def setUp(self):
        self.data_adapter = MemoryDataAdapter()
        self.state_provider.data_adapter = self.data_adapter

        self.chat = Chat()
        self.chat.id = 101
        self.user = User()
        self.user.id = 111

        state_data1 = {"state": "main", "state_type": "reserve"}
        state_data2 = {"state": "book", "state_type": "reserve"}
        self.data_adapter.append_data("101-111-121", state_data1)
        self.data_adapter.append_data("101-111-122", state_data2)

    async def test_message_default(self):
        """Default message state"""
        test_message = Message()
        test_message.chat = self.chat
        test_message.from_user = self.user
        test_message.message_id = 123

        await self.message_default(test_message)

        passed, alert = self.assert_params(self.result_text, "Default message")
        assert passed, alert

    async def test_message_reserve_main(self):
        """Reserve state main message"""

        test_message = Message()
        test_message.chat = self.chat
        test_message.from_user = self.user
        test_message.message_id = 121
        test_message.text = "Message-121"

        await self.message_reserve_main(test_message)

        passed, alert = self.assert_params(self.result_text,
                                           "Message-121: reserve main")
        assert passed, alert

    async def test_callback_query_reserve_book(self):
        """Reserve state main message"""
        test_message = Message()
        test_message.chat = self.chat
        test_message.from_user = self.user
        test_message.message_id = 122

        test_callback_query = CallbackQuery()
        test_callback_query.message = test_message

        await self.callback_query_reserve_book(test_callback_query)
        passed, alert = self.assert_params(self.result_text,
                                           "Callback: reserve book")
        assert passed, alert
