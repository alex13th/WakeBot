from bot_tests.data.t_state import StateManagerTestCase
from bot_tests.data.t_state import StateProviderTestCase
from bot_tests.data.t_adapters import MemoryDataAdapterTestCase
from bot_tests.entities import ReserveTestCase, UserTestCase
from bot_tests.processors import DefaultProcessorTestCase
from bot_tests.processors import ReserveProcessorTestCase
from bot_tests.processors import WakeProcessorTestCase

test_count = fail_count = 0

tests, fails = StateManagerTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = StateProviderTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = MemoryDataAdapterTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = UserTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = ReserveTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = DefaultProcessorTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = ReserveProcessorTestCase().run_tests_async()
test_count += tests
fail_count += fails

tests, fails = WakeProcessorTestCase().run_tests_async()
test_count += tests
fail_count += fails

print(f"\nRan {test_count} test (failure = {fail_count}) ")
