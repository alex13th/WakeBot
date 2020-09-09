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
        canceled:
            Optional. A boolean meaning that a reserevation is canceled
        cancel_telegram_id:
            Optional. An integer telegram identifier
            of user canceled a reserevation
    """

    __slots__ = ["board", "hydro"]

    def __init__(self,
                 user: Optional[User] = None,
                 start_date: Optional[date] = None,
                 start_time: Optional[time] = None,
                 set_type_id: str = "set",
                 set_count: int = 1,
                 count: int = 1,
                 id: Union[int, None] = None,
                 board: Optional[int] = 0,
                 hydro: Optional[int] = 0,
                 canceled: Union[bool, None] = False,
                 cancel_telegram_id: Union[int, None] = None):
        """Wakeboard reservation data class

        Args:
            user:
                Optional. A instance of User class object.
            start_date:
                Optional. Wakeboard reservation start date only.
            start_time:
                Optional. Wakeboard reservation start time only.
            set_type:
                A reservation set type instances.
            set_count:
                A integer value of set's count.
            id:
                An integer wakeboard reservation identifier
            boad:
                An integer value of a wakeboard equipment rent need
            hydro:
                An integer value of a hydrosuite equipment rent need
            id:
                An integer wakeboard reservation identifier
            canceled:
                Optional. A boolean meaning that a reserevation is canceled
            cancel_telegram_id:
                Optional. An integer telegram identifier
                of user canceled a reserevation
        """
        super().__init__(user=user,
                         start_date=start_date, start_time=start_time,
                         set_type_id=set_type_id, set_count=set_count,
                         count=count, id=id,
                         canceled=canceled,
                         cancel_telegram_id=cancel_telegram_id)

        if set_type_id == "hour":
            self.set_type = ReserveSetType(set_type_id, 60)
        else:
            self.set_type = ReserveSetType(set_type_id, 10)

        self.board = board
        self.hydro = hydro

    def __copy__(self):
        return Wake(self.user, self.start_date, self.start_time,
                    self.set_type.set_id, self.set_count,
                    self.count, self.id,
                    self.board, self.hydro)

    def __eq__(self, other) -> bool:
        if (self.start == other.start
                and self.count == other.count
                and self.set_count == other.set_count
                and self.minutes == other.minutes
                and self.board == other.board
                and self.hydro == other.hydro):
            return True
        else:
            return False

    def __repr__(self) -> str:
        """Provide built-in mapping to represantation string"""
        return (f"Wake(start_date={self.start_date!r}, "
                f"start_time={self.start_time!r}, "
                f"set_type={self.set_type.name!r}, "
                f"set_count={self.set_count}, "
                f"minutes={self.minutes}, "
                f"board={self.board}, "
                f"hydro={self.hydro}, "
                f"is_complete={self.is_complete})")


if __name__ == "__main__":
    test = Wake()
