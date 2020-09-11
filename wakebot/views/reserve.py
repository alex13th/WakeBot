from typing import Optional, Iterator

from ..entities import Reserve
from .strings import ReserveTelegramStrings


class ReserveTelegramView:
    """Reservation telegram message generator

    Attributes:
        strings:
            A local stings class.
    """

    __slots__ = ["strings"]

    def __init__(self, strings: Optional[ReserveTelegramStrings] = None):
        """Reservation telegram message generator

        Args:
        strings:
            A local stings class.
        """
        self.strings = strings if strings else ReserveTelegramStrings

    def create_booking_info(self,
                            reserve: Reserve,
                            show_contact: bool = False) -> str:
        """Create a book menu text
        Args:
            show_contact:
                Optional. A boolean value means to allow
                show contact information

        Returns:
            A message text.
        """

        result = (f"{self.strings.service_label} "
                  f"{self.strings.service_type_text}\n")

        if reserve.user and show_contact:
            result += f"{self.strings.name_label} {reserve.user.displayname}\n"
            if reserve.user.phone_number:
                result += (f"{self.strings.phone_label} "
                           f"{reserve.user.phone_number}\n")

        result += (f"{self.strings.date_label} "
                   f"{reserve.start_date.strftime(self.strings.date_format)}"
                   "\n")

        if reserve.start_time:
            start_time = reserve.start_time.strftime(self.strings.time_format)
            result += (f"{self.strings.start_label} "
                       f"{start_time}\n")
            end_time = reserve.end_time.strftime(self.strings.time_format)
            result += (f"{self.strings.end_label} "
                       f"{end_time}\n")

        result += (f"{self.strings.set_type_label} "
                   f"{self.strings.set_types[reserve.set_type.set_id]}"
                   f" ({reserve.set_count})\n")

        result += (f"{self.strings.count_label} "
                   f"{reserve.count}\n")

        return result

    def create_hello_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """

        return self.strings.hello_message

    def create_list_text(self, reserve_list: Iterator[Reserve] = None) -> str:
        """Create list menu InlineKeyboardMarkup
        Args:
            reserve_list:
                A list of reservation instances

        Returns:
            A list menu text.
        """

        if not reserve_list:
            return self.strings.list_empty

        result = f"{self.strings.list_header}\n"

        cur_date = None
        i = 0
        for reserve in reserve_list:
            if not cur_date or cur_date != reserve.start_date:
                cur_date = reserve.start_date
                result += f"*{cur_date.strftime(self.strings.date_format)}*\n"

            i += 1
            result += (f"  {i}. {self.create_reserve_text(reserve)}\n")

        return result

    def create_reserve_text(self, reserve: Reserve) -> str:
        result = ""
        start_time = reserve.start_time.strftime(self.strings.time_format)
        end_time = reserve.end_time.strftime(self.strings.time_format)
        result += f"  {start_time} - {end_time}"

        return result
