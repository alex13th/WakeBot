# -*- coding: utf-8 -*-
import unittest
from datetime import date, time, datetime, timedelta

from wakebot.entities.reserve import Reserve
from wakebot.entities.user import User


class ReserveTestCase(unittest.TestCase):
    """Тесты модуля произвольного резервирования """

    def setUp(self):
        self.user = User("Firstname")
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.minutes = 30  # продолжительность
        self.reserve = Reserve(self.user, self.start_date,
                               self.start_time, self.minutes)

    def check_reserve(self, reserve, start_reserve, end_reserve,
                      minutes, user):
        self.assertEqual(reserve.start, start_reserve)
        self.assertEqual(reserve.end, end_reserve)
        self.assertEqual(reserve.start_date, start_reserve.date())
        self.assertEqual(reserve.start_time, start_reserve.time())
        self.assertEqual(reserve.end_date, end_reserve.date())
        self.assertEqual(reserve.end_time, end_reserve.time())
        self.assertEqual(reserve.minutes, minutes)
        self.assertEqual(reserve.user, user)

    def test_default_properties(self):
        """Созданиен объекта со свойствами по умолчению"""
        reserve = Reserve()

        self.assertIsNone(reserve.start)
        self.assertIsNone(reserve.start_date)
        self.assertIsNone(reserve.start_time)
        self.assertIsNone(reserve.end)
        self.assertIsNone(reserve.end_date)
        self.assertIsNone(reserve.end_time)
        self.assertIsNone(reserve.user)

    def test_create_with_properties(self):
        """Создания объекта со свойствами"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user
        start_reserve = datetime.combine(self.start_date, self.start_time)
        end_reserve = start_reserve + timedelta(minutes=self.minutes)

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    def test_change_start(self):
        """Изменение времени начала резервирования"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user

        # Сохраняет продолжительность
        start_reserve = datetime.combine(date.today(), time(15, 0, 0))
        end_reserve = datetime.combine(date.today(), time(15, minutes, 0))
        reserve.start = start_reserve

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    def test_change_end(self):
        """Изменение времени окончания резервирования"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user

        # Сохраняет продолжительность
        start_reserve = datetime.combine(date.today(), time(18, 0, 0))
        end_reserve = datetime.combine(date.today(), time(18, minutes, 0))
        reserve.start = start_reserve

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    def test_change_minutes(self):
        """Изменение продолжительности резервирования"""
        reserve = self.reserve
        start = datetime.combine(self.start_date, self.start_time)
        user = self.user

        # Изменяет окончание
        minutes = 40
        start_reserve = start
        end_reserve = start + timedelta(minutes=40)
        reserve.minutes = minutes

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    def test_to_str_incomplete(self):
        """Строка незавершенного резервирования"""
        reserve = Reserve()
        self.assertEqual(str(reserve), "")

    def test_to_str_oneday(self):
        """Строка однодневного резервирования"""
        reserve = self.reserve

        reserve_str = "{}: {} - {}".format(reserve.start_date,
                                           reserve.start_time,
                                           reserve.end_time)
        self.assertEqual(str(reserve), reserve_str)

    def test_to_str_multiday(self):
        """Строка многодневного резервирования"""
        reserve = self.reserve
        reserve.minutes = 1500

        reserve_str = "{} {} - {} {}".format(reserve.start_date,
                                             reserve.start_time,
                                             reserve.end_date,
                                             reserve.end_time)
        self.assertEqual(str(reserve), reserve_str)


try:
    unittest.main()
except SystemExit:
    pass
