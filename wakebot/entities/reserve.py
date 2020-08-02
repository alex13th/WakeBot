# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date, time


class ReserveSetType():
    """Reservation set type class defines reservation time duration"""

    def __init__(self, set_id="minute", minutes=1):
        self.set_id = set_id
        self.minutes = minutes


class Reserve:
    """Reservation data class

    Attributes:
        is_complete:
            A boolean attribute indicates that reservation is complete or not.
        user:
            A instance of User class object.
        start:
            Reservation start datetime.
        start_date:
            Reservation start date only.
        start_time:
            Reservation start time only.
        end:
            Reservation end datetime.
        end_date:
            Reservation end date only.
        end_time:
            Reservation end time only.
        set_type:
            A reservation set type instances.
        set_count:
            A integer value of set's count.
    """

    def __init__(self, user=None, start_date=None,
                 start_time=None, set_type=None, set_count=1):
        """Reservation data class

        Args:
            user:
                Optional. A instance of User class object.
            start_date:
                Optional. Reservation start date only.
            start_time:
                Optional. Reservation start time only.
            set_type:
                A reservation set type instances.
            set_count:
                A integer value of set's count.
        """
        if not set_type:
            set_type = ReserveSetType("set", 5)
        self.__user = user
        self.__start_date = start_date
        self.__start_time = start_time
        self.set_type = set_type
        self.set_count = set_count

    @property
    def is_complete(self):
        """Информация о клиенте"""
        return self.__start_date and self.__start_time and self.minutes

    @property
    def user(self):
        """Информация о клиенте"""
        return self.__user

    @property
    def start(self):
        """Дата и время начала резервирования"""
        if not (self.__start_date and self.__start_time):
            return None

        return datetime.combine(self.__start_date, self.__start_time)

    @start.setter
    def start(self, value):
        self.__start_date = value.date()
        self.__start_time = value.time()

    @property
    def start_date(self):
        """Дата время начала резервирования"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        """Дата время начала резервирования"""
        self.__start_date = value

    @property
    def start_time(self):
        """Время начала резервирования"""
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        """Время начала резервирования"""
        self.__start_time = value

    @property
    def minutes(self):
        """Время начала резервирования"""
        return self.set_type.minutes * self.set_count

    @property
    def end(self):
        """Дата и время окончания резервирования"""
        result = None
        if self.is_complete:
            result = datetime.combine(self.__start_date, self.__start_time)
            result += timedelta(minutes=self.minutes)

        return result

    @property
    def end_date(self):
        """Дата окончания резервирования"""
        result = None
        if self.is_complete:
            result = datetime.combine(self.__start_date, self.__start_time)
            result += timedelta(minutes=self.minutes)
            result = result.date()

        return result

    @property
    def end_time(self):
        """Время окончания резервирования"""
        result = None
        if self.__start_date and self.__start_time and self.minutes:
            result = datetime.combine(self.__start_date, self.__start_time)
            result += timedelta(minutes=self.minutes)
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

    def __eq__(self, other):
        if (self.start_date == other.start_date
           and self.set_count == other.set_count
           and self.minutes == other.minutes):
            return True
        else:
            return False


if __name__ == "__main__":
    reserve = Reserve(None, date.today(), time(), 30)
    print(reserve)
