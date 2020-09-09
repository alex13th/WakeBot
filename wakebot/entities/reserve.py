from datetime import datetime, timedelta, date, time
from typing import Optional, Union

from .user import User


class ReserveSetType():
    """Reservation set type class defines reservation time duration"""

    __slots__ = ["set_id", "minutes", "name"]

    def __init__(self, set_id="minute", minutes=1, name=None):
        self.set_id = set_id
        self.minutes = minutes
        self.name = name if name else set_id


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
            An integer value of set's count.
        count:
            An integer value of count reservation pieces
        id:
            An integer wakeboard reservation identifier
        canceled:
            A boolean meaning that a reserevation is canceled
        cancel_telegram_id:
            An integer telegram identifier of user canceled a reserevation
    """

    __slots__ = ["id", "user", "start_date", "start_time", "set_type",
                 "set_count", "count", "canceled", "cancel_telegram_id"]

    def __init__(self,
                 user: Optional[User] = None,
                 start_date: Optional[date] = None,
                 start_time: Optional[time] = None,
                 set_type_id: str = "set",
                 set_count: int = 1, count: int = 1,
                 id: Union[int, None] = None,
                 canceled: Union[bool, None] = False,
                 cancel_telegram_id: Union[int, None] = None):
        """Reservation data class

        Args:
            user:
                Optional. A instance of User class object.
            start_date:
                Optional. Reservation start date only.
            start_time:
                Optional. Reservation start time only.
            set_type:
                Optional. A reservation set type instances.
            set_count:
                A integer value of set's count.
            count:
                A integer value of equipment count.
            id:
                Optional. An integer wakeboard reservation identifier
            canceled:
                Optional. A boolean meaning that a reserevation is canceled
            cancel_telegram_id:
                Optional. An integer telegram identifier
                of user canceled a reserevation
        """
        if set_type_id == "hour":
            self.set_type = ReserveSetType(set_type_id, 60)
        else:
            self.set_type = ReserveSetType(set_type_id, 5)

        self.user = user
        self.start_date = start_date if start_date else date.today()
        self.start_time = start_time
        self.set_count = set_count
        self.count = count
        self.id = id
        self.canceled = bool(canceled)
        self.cancel_telegram_id = cancel_telegram_id

    @property
    def is_complete(self) -> bool:
        return bool(self.start_date
                    and self.start_time
                    and self.minutes
                    and self.user and self.user.phone_number)

    @property
    def start(self) -> Optional[datetime]:
        if not (self.start_date and self.start_time):
            return None

        return datetime.combine(self.start_date, self.start_time)

    @start.setter
    def start(self, value: Optional[datetime]):
        self.start_date = value.date()
        self.start_time = value.time()

    @property
    def end(self) -> Optional[datetime]:
        result = None
        if self.start_date and self.start_time and self.minutes:
            result = datetime.combine(self.start_date, self.start_time)
            result += timedelta(minutes=self.minutes)

        return result

    @property
    def end_date(self) -> Optional[date]:
        result = None
        if self.start_date and self.start_time and self.minutes:
            result = datetime.combine(self.start_date, self.start_time)
            result += timedelta(minutes=self.minutes)
            result = result.date()

        return result

    @property
    def end_time(self) -> Optional[time]:
        result = None
        if self.start_date and self.start_time and self.minutes:
            result = datetime.combine(self.start_date, self.start_time)
            result += timedelta(minutes=self.minutes)
            result = result.time()

        return result

    @property
    def minutes(self) -> int:
        return self.set_type.minutes * self.set_count

    def check_concurrent(self, other) -> int:
        """Check reservation time conflict

        Returns:
            Count of reservations is conflicted.
        """
        if self.start == other.start:
            return self.count + other.count

        if (self.start < other.start and self.end > other.start):
            return self.count + other.count

        if (self.start > other.start and
                self.start < other.end):
            return self.count + other.count

        return self.count

    def __str__(self) -> str:
        """Provide built-in mapping to string"""
        if not self.is_complete:
            return ""
        elif self.start_date == self.end_date:
            return f"{self.start_date}: {self.start_time} - {self.end_time}"
        elif self.start_date != self.end_date:
            return "{} {} - {} {}".format(self.start_date,
                                          self.start_time,
                                          self.end_date,
                                          self.end_time)

    def __repr__(self) -> str:
        """Provide built-in mapping to represantation string"""
        return (f"Reservation(start_date={self.start_date!r}, "
                f"start_time={self.start_time!r}, "
                f"set_type={self.set_type.name!r}, "
                f"set_count={self.set_count}, "
                f"minutes={self.minutes}, "
                f"is_complete={self.is_complete})")

    def __eq__(self, other) -> bool:
        """Provide built-in comparation to other reserve instance"""
        if (self.start == other.start
                and self.count == other.count
                and self.set_count == other.set_count
                and self.minutes == other.minutes):
            return True
        else:
            return False

    def __copy__(self, other):
        return Reserve(self.user, self.start_date, self.start_time,
                       self.set_type.set_id, self.set_count, self.count,
                       self.id)
