from ..base_test_case import BaseTestCase
from datetime import date, time, datetime, timedelta

from wakebot.entities import Reserve, User


class ReserveTestCase(BaseTestCase):
    """Тесты модуля произвольного резервирования """

    def setUp(self):
        self.user = User("Firstname", phone_number="+777")
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.minutes = 5  # продолжительность
        self.reserve = Reserve(self.user, self.start_date,
                               self.start_time)

    def check_reserve(self, reserve, start_reserve, end_reserve,
                      minutes, user):
        passed, alert = self.assert_params(reserve.start, start_reserve)
        assert passed, alert
        passed, alert = self.assert_params(reserve.end, end_reserve)
        assert passed, alert
        passed, alert = self.assert_params(reserve.start_date,
                                           start_reserve.date())
        assert passed, alert
        passed, alert = self.assert_params(reserve.start_time,
                                           start_reserve.time())
        assert passed, alert
        passed, alert = self.assert_params(reserve.end_date,
                                           end_reserve.date())
        assert passed, alert
        passed, alert = self.assert_params(reserve.end_time,
                                           end_reserve.time())
        assert passed, alert
        passed, alert = self.assert_params(reserve.minutes,
                                           minutes)
        assert passed, alert
        passed, alert = self.assert_params(reserve.user,
                                           user)
        assert passed, alert

    async def test_create_with_properties(self):
        """Создания объекта со свойствами"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user
        start_reserve = datetime.combine(self.start_date, self.start_time)
        end_reserve = start_reserve + timedelta(minutes=self.minutes)

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_change_start(self):
        """Изменение времени начала резервирования"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user

        # Сохраняет продолжительность
        start_reserve = datetime.combine(date.today(), time(15, 0, 0))
        end_reserve = datetime.combine(date.today(), time(15, minutes, 0))
        reserve.start = start_reserve

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_change_end(self):
        """Изменение времени окончания резервирования"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user

        # Сохраняет продолжительность
        start_reserve = datetime.combine(date.today(), time(18, 0, 0))
        end_reserve = datetime.combine(date.today(), time(18, minutes, 0))
        reserve.start = start_reserve

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_change_minutes(self):
        """Изменение продолжительности резервирования"""
        reserve = self.reserve
        start = datetime.combine(self.start_date, self.start_time)
        user = self.user

        # Изменяет окончание
        minutes = 40
        start_reserve = start
        end_reserve = start + timedelta(minutes=40)
        reserve.set_count = 8

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_to_str_incomplete(self):
        """Строка незавершенного резервирования"""
        reserve = Reserve()
        passed, alert = self.assert_params(str(reserve), "")
        assert passed, alert

    async def test_to_str_oneday(self):
        """Строка однодневного резервирования"""
        reserve = self.reserve

        reserve_str = "{}: {} - {}".format(reserve.start_date,
                                           reserve.start_time,
                                           reserve.end_time)
        passed, alert = self.assert_params(str(reserve), reserve_str)
        assert passed, alert

    async def test_to_str_multiday(self):
        """Строка многодневного резервирования"""
        reserve = self.reserve
        reserve.set_count = 300

        reserve_str = "{} {} - {} {}".format(reserve.start_date,
                                             reserve.start_time,
                                             reserve.end_date,
                                             reserve.end_time)
        passed, alert = self.assert_params(str(reserve), reserve_str)
        assert passed, alert

    async def test_equal(self):
        """Реализация сравнения резервирований"""
        reserve1 = Reserve(self.user, self.start_date,
                           self.start_time)

        passed, alert = self.assert_params(reserve1, self.reserve)
        assert passed, alert

        reserve1 = Reserve(self.user, self.start_date,
                           self.start_time, set_count=2)
        passed, alert = self.assert_params(reserve1, self.reserve)
        assert not passed, alert

    async def test_check_concurrent(self):
        """Реализация сравнения резервирований"""
        start_time = time(12, 00)
        reserve1 = Reserve(self.user, start_date=self.start_date,
                           start_time=start_time, count=2, set_count=12)
        reserve2 = Reserve(self.user, start_date=self.start_date,
                           count=3, set_count=3)

        reserve2.start_time = time(11, 30)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 2)
        assert passed, alert

        reserve2.start_time = time(11, 45)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 2)
        assert passed, alert

        reserve2.start_time = time(11, 55)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 5)
        assert passed, alert

        reserve2.start_time = time(12, 00)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 5)
        assert passed, alert

        reserve2.start_time = time(12, 10)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 5)
        assert passed, alert

        reserve2.start_time = time(12, 45)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 5)
        assert passed, alert

        reserve2.start_time = time(12, 55)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 5)
        assert passed, alert

        reserve2.start_time = time(13, 00)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 2)
        assert passed, alert

        reserve2.start_time = time(13, 5)
        conflict_count = reserve1.check_concurrent(reserve2)
        passed, alert = self.assert_params(conflict_count, 2)
        assert passed, alert
