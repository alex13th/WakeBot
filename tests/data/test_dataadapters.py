# -*- coding: utf-8 -*-
import unittest
from wakebot.adapters.data import MemoryDataAdapter


class MemoryDataAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.adapter = MemoryDataAdapter()

    def test_create_object(self):
        self.assertIsInstance(self.adapter.storage, dict)

    def test_append_data(self):
        data = {"attr": "attr_value"}

        self.adapter.append_data("test_key", data)
        self.assertEqual(self.adapter.storage["test_key"], data)

    def test_get_data(self):
        data1 = {"data_attr1": "data_value1"}
        data2 = {"data_attr2": "data_value2"}
        data3 = {"data_attr3": "data_value3"}
        data4 = {"data_attr4": "data_value4"}
        data5 = {"data_attr5": "data_value5"}

        self.adapter.append_data("key1", data1)
        self.adapter.append_data("key2", data2)
        self.adapter.append_data("key3", data3)
        self.adapter.append_data("key4", data4)
        self.adapter.append_data("key4", data5)

        self.assertEqual(len(self.adapter.get_data()), 4)
        self.assertEqual(self.adapter.get_data()["key1"], data1)
        self.assertEqual(self.adapter.get_data()["key2"], data2)
        self.assertEqual(self.adapter.get_data()["key3"], data3)
        self.assertEqual(self.adapter.get_data()["key4"], data5)

    def test_get_data_by_keys(self):
        data1 = {"data_attr1": "data_value1"}
        data2 = {"data_attr2": "data_value2"}
        data3 = {"data_attr3": "data_value3"}
        data4 = {"data_attr4": "data_value4"}
        data5 = {"data_attr5": "data_value5"}

        self.adapter.append_data("key1", data1)
        self.adapter.append_data("key2", data2)
        self.adapter.append_data("key3", data3)
        self.adapter.append_data("key4", data4)
        self.adapter.append_data("key4", data5)

        self.assertEqual(self.adapter.get_data_by_keys("key1"), data1)
        self.assertEqual(self.adapter.get_data_by_keys("key2"), data2)
        self.assertEqual(self.adapter.get_data_by_keys("key3"), data3)
        self.assertEqual(self.adapter.get_data_by_keys("key4"), data5)


try:
    unittest.main()
except SystemExit:
    pass
