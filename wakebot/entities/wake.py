from typing import Optional, Union
from datetime import date, time
from .reserve import Reserve, ReserveSetType
from .user import User


class Wake(Reserve):
    """Wakeboard reservation data class

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
            A string value indicates type of set ("set", "hour").
        set_count:
            A integer value of set's count.
        boad:
            An integer value of a wakeboard equipment rent need
        hydro:
            An integer value of a hydrosuite equipment rent need
    """

    def __init__(self,
                 user: Optional[User] = None,
                 start_date: Optional[date] = None,
                 start_time: Optional[time] = None,
                 set_type: Union[str, int, None] = None,
                 set_count: Optional[int] = 1,
                 board: Optional[int] = 0,
                 hydro: Optional[int] = 0):
        """Wakeboard reservation data class

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
            boad:
                An integer value of a wakeboard equipment rent need
            hydro:
                An integer value of a hydrosuite equipment rent need
        """
        if not set_type:
            set_type = ReserveSetType("set", 10)

        super().__init__(user, start_date, start_time, set_type, set_count)
        self.board = board
        self.hydro = hydro

    def __eq__(self, other) -> bool:
        """Provide a built-in object comparation"""
        if (self.start_date == other.start_date
           and self.set_count == other.set_count
           and self.minutes == other.minutes
           and self.board == other.board
           and self.hydro == other.hydro):
            return True
        else:
            return False


if __name__ == "__main__":
    test = Wake()
