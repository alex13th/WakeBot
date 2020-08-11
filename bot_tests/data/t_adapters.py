from ..base_test_case import BaseTestCase
from wakebot.adapters.data import MemoryDataAdapter


class MemoryDataAdapterTestCase(BaseTestCase):
    """MemoryDataAdapter class"""
    
    def setUp(self):
        self.adapter = MemoryDataAdapter()

    async def test_append_data(self):
        data = {"attr": "attr_value"}

        self.adapter.append_data("test_key", data)

        passed, alert = self.assert_params(self.adapter.storage["test_key"],
                                           data)
        assert passed, alert

    async def test_get_data(self):
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

        data_rows = self.adapter.get_data()

        passed, alert = self.assert_params(len(data_rows), 4)
        assert passed, alert
        passed, alert = self.assert_params(data_rows["key1"], data1)
        assert passed, alert
        passed, alert = self.assert_params(data_rows["key2"], data2)
        assert passed, alert
        passed, alert = self.assert_params(data_rows["key3"], data3)
        assert passed, alert
        passed, alert = self.assert_params(data_rows["key4"], data5)
        assert passed, alert

    async def test_get_data_by_keys(self):
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

        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys("key1"), data1)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys("key2"), data2)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys("key3"), data3)
        assert passed, alert
        passed, alert = self.assert_params(
            self.adapter.get_data_by_keys("key4"), data5)
        assert passed, alert
