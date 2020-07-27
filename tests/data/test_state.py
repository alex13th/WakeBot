# -*- coding: utf-8 -*-
import unittest
from wakebot.adapters.state import StateManager
from wakebot.adapters.data import MemoryDataAdapter


class MemoryDataAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.data_adapter = MemoryDataAdapter()

        state_data = {"state": "main", "state_type": "reserve"}
        self.data_adapter.append_data("101-111-122", state_data)
        self.data_adapter.append_data("101-111-122", state_data)

    def test_create_object(self):
        state_mgr = StateManager(self.data_adapter, 101, 111)

        self.assertEqual(state_mgr.data_adapter, self.data_adapter)
        self.assertEqual(state_mgr.state_id, "101-111")
        self.assertEqual(state_mgr.state_type, "")
        self.assertEqual(state_mgr.state, "")

    def test_create_object_with_message(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 121)

        self.assertEqual(state_mgr.state_id, "101-111-121")
        self.assertEqual(state_mgr.state_type, "")
        self.assertEqual(state_mgr.state, "")

    def test_create_object_with_storied(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 122)

        self.assertEqual(state_mgr.state_id, "101-111-122")
        self.assertEqual(state_mgr.state_type, "reserve")
        self.assertEqual(state_mgr.state, "main")

    def test_change_state(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 122)

        state_mgr.set_state("book")

        self.assertEqual(state_mgr.state_id, "101-111-122")
        self.assertEqual(state_mgr.state_type, "reserve")
        self.assertEqual(state_mgr.state, "book")

    def test_change_state_type(self):
        state_mgr = StateManager(self.data_adapter, 101, 111, 122)

        state_mgr.set_state(state_type="reserve1")

        self.assertEqual(state_mgr.state_id, "101-111-122")
        self.assertEqual(state_mgr.state_type, "reserve1")
        self.assertEqual(state_mgr.state, "main")

    def test_set_state(self):
        state_mgr = StateManager(self.data_adapter, 101, 111)

        state_mgr.set_state("book2", "reserve2", 122)
        state_data = self.data_adapter.get_data_by_keys("101-111-122")

        self.assertEqual(state_data["state_type"], "reserve2")
        self.assertEqual(state_data["state"], "book2")


try:
    unittest.main()
except SystemExit:
    pass
