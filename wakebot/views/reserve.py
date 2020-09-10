from typing import Optional
from wakebot.views import ReserveTelegramStrings


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

    def create_hello_text(self) -> str:
        """Create a main menu text

        Returns:
            A message text.
        """

        return self.strings.hello_message
