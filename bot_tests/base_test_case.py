# -*- coding: utf-8 -*-
import asyncio
import sys
import traceback


class BaseTestCase():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def assert_params(self, value, expected_value):
        passed = value == expected_value
        return (passed, self.get_failure_text(value, expected_value))

    def setUp(self):
        pass

    def print_success(self, test_name):
        print(f"{test_name}: {self.OKGREEN}SUCCESS{self.ENDC}")

    def print_failure(self, test_name, error):
        print(f"{test_name}: {self.FAIL}FAILED{self.ENDC}\n"
              + " " * 4 + f"{error}")

    def print_error(self, test_name, error):
        print(f"{test_name}: {self.FAIL}ERROR{self.ENDC}\n"
              f"{self.BOLD}{error}{self.ENDC}")

    def get_failure_text(self, result_value, expected_value):
        return (" " * 4 + f"{self.BOLD}Expected:{self.ENDC}\n"
                + f"'{result_value}'\n"
                + " " * 4 + f" {self.BOLD}Equal to:{self.ENDC}\n'"
                + f"{expected_value}'")

    def run_tests_async(self):
        method_list = [getattr(self, test) for test in dir(self)
                       if test.startswith("test_")
                       and callable(getattr(self, test))]

        header = (f"\n{'*'*5} {self.BOLD}Starting tests:{self.ENDC} "
                  f"{self.__doc__} {'*'*5}\n")
        footer = (f"\n{'*'*5} {self.BOLD}End tests:{self.ENDC} "
                  f"{self.__doc__} {'*'*5}\n")

        print(header)
        fail_count = 0

        for test in method_list:
            self.setUp()
            test_name = test.__doc__ if test.__doc__ else test.__name__

            try:
                asyncio.run(test())
                self.print_success(test_name)
            except AssertionError as assert_error:
                _, _, tb = sys.exc_info()
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]

                self.print_failure(test_name, (f"{assert_error}\n"
                                               + f"(line: {line},"
                                               + f"file name: {filename})\n"))
                fail_count += 1
            except Exception:
                self.print_error(test_name, "\n".join(
                                 traceback.format_exc().splitlines()))
                fail_count += 1

        print(f"\nRan {len(method_list)} test (failure = {fail_count}) ")
        print(footer)

        return len(method_list), fail_count
