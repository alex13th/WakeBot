# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date, time


class Reserve:
    """
    Базовый класс моделей резервирования
    """

    def __init__(self, user=None, start_date=None,
                 start_time=None, minutes=None):
        self._user = user
        self._start_date = start_date
        self._start_time = start_time
        self._minutes = minutes

    @property
    def is_complete(self):
        """Информация о клиенте"""
        return self._start_date and self._start_time and self._minutes

    @property
    def user(self):
        """Информация о клиенте"""
        return self._user

    @property
    def start(self):
        """Дата и время начала резервирования"""
        if not (self._start_date and self._start_time):
            return None

        return datetime.combine(self._start_date, self._start_time)

    @start.setter
    def start(self, value):
        self._start_date = value.date()
        self._start_time = value.time()

    @property
    def start_date(self):
        """Дата время начала резервирования"""
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        """Дата время начала резервирования"""
        self._start_date = value

    @property
    def start_time(self):
        """Время начала резервирования"""
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """Время начала резервирования"""
        self._start_time = value

    @property
    def minutes(self):
        """Время начала резервирования"""
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        """Время начала резервирования"""
        self._minutes = value

    @property
    def end(self):
        """Дата и время окончания резервирования"""
        result = None
        if self.is_complete:
            result = datetime.combine(self.start_date, self._start_time)
            result += timedelta(minutes=self._minutes)

        return result

    @property
    def end_date(self):
        """Дата окончания резервирования"""
        result = None
        if self.is_complete:
            result = datetime.combine(self._start_date, self._start_time)
            result += timedelta(minutes=self._minutes)
            result = result.date()

        return result

    @property
    def end_time(self):
        """Время окончания резервирования"""
        result = None
        if self._start_date and self._start_time and self._minutes:
            result = datetime.combine(self.start_date, self._start_time)
            result += timedelta(minutes=self._minutes)
            result = result.time()

        return result

    def __str__(self):
        if not self.is_complete:
            return ""
        elif self.start_date == self.end_date:
            return f"{self.start_date}: {self.start_time} - {self.end_time}"
        elif self.start_date != self.end_date:
            return "{} {} - {} {}".format(self.start_date,
                                          self.start_time,
                                          self.end_date,
                                          self.end_time)
        else:
            raise Exception


if __name__ == "__main__":
    reserve = Reserve(None, date.today(), time(), 30)
    print(reserve)
