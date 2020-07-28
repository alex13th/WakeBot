# -*- coding: utf-8 -*-
import asyncio


class BaseTestCase():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def assertEqual(self, value, expected_value):
        passed = value and value == expected_value
        assert passed, self.get_failure_text(value, expected_value)

    def setUp(self):
        raise NotImplementedError

    def print_success(self, test_name):
        print(f"{test_name}: {self.OKGREEN}SUCCESS{self.ENDC}")

    def print_failure(self, test_name, error):
        print(f"{test_name}: {self.FAIL}FAILED{self.ENDC}\n"
              + " " * 4 + f"{error}")

    def print_error(self, test_name, error):
        print(f"{test_name}: {self.FAIL}ERROR{self.ENDC}\n"
              + " " * 4 + f"{self.BOLD}{error}{self.ENDC}")

    def get_failure_text(self, result_value, expected_value):
        return (f"{self.BOLD}Expected:{self.ENDC} '{result_value}'"
                f" {self.BOLD}equal{self.ENDC} '{expected_value}'")

    def run_tests_async(self):
        method_list = [getattr(self, test) for test in dir(self)
                       if test.startswith("test_")
                       and callable(getattr(self, test))]

        fail_count = 0
        for test in method_list:
            self.setUp()
            test_name = test.__doc__ if test.__doc__ else test.__name__

            try:
                asyncio.run(test())
                self.print_success(test_name)
            except AssertionError as assert_error:
                self.print_failure(test_name, assert_error)
                fail_count += 1
            except Exception as error:
                self.print_error(test_name, error)
                fail_count += 1

        print(f"\nRan {len(method_list)} test (failure = {fail_count}) ")
