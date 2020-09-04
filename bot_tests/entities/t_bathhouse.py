from ..base_test_case import BaseTestCase
from datetime import date, time, datetime, timedelta

from wakebot.entities import Bathhouse, User


class BathhouseTestCase(BaseTestCase):
    """A Bathhouse class tests """

    def setUp(self):
        self.user = User("Firstname", phone_number="+777")
        self.start_date = date.today()
        self.start_time = time(10, 0, 0)
        self.minutes = 60  # продолжительность
        self.set_count = 1
        self.reserve = Bathhouse(self.user, self.start_date, self.start_time,
                                 set_count=1, count=2)

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
        passed, alert = self.assert_params(reserve.count,
                                           2)
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
        end_reserve = datetime.combine(date.today(), time(16, 0, 0))
        reserve.start = start_reserve

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_change_end(self):
        """Изменение времени окончания резервирования"""
        reserve = self.reserve
        minutes = self.minutes
        user = self.user

        # Сохраняет продолжительность
        start_reserve = datetime.combine(date.today(), time(18, 0, 0))
        end_reserve = datetime.combine(date.today(), time(19, 0, 0))
        reserve.start = start_reserve

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_change_minutes(self):
        """Изменение продолжительности резервирования"""
        reserve = self.reserve
        start = datetime.combine(self.start_date, self.start_time)
        user = self.user

        # Изменяет окончание
        minutes = 240
        start_reserve = start
        end_reserve = start + timedelta(minutes=240)
        reserve.set_count = 4

        self.check_reserve(reserve, start_reserve, end_reserve, minutes, user)

    async def test_to_str_incomplete(self):
        """Строка незавершенного резервирования"""
        reserve = Bathhouse()
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
        reserve.set_count = 150

        reserve_str = "{} {} - {} {}".format(reserve.start_date,
                                             reserve.start_time,
                                             reserve.end_date,
                                             reserve.end_time)
        passed, alert = self.assert_params(str(reserve), reserve_str)
        assert passed, alert

    async def test_equal(self):
        """Реализация сравнения резервирований"""
        reserve1 = Bathhouse(self.user, self.start_date, self.start_time,
                             set_count=1, count=2)

        passed, alert = self.assert_params(reserve1, self.reserve)
        assert passed, alert

        reserve1 = Bathhouse(self.user, self.start_date,
                             self.start_time, set_count=3)
        passed, alert = self.assert_params(reserve1, self.reserve)
        assert not passed, alert
