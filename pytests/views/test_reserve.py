import pytest

from wakebot.views.reserve import ReserveTelegramView
from wakebot.views import ReserveTelegramStrings
from wakebot.views import RuReserveTelegramStrings


@pytest.mark.reserve
@pytest.mark.telegram
@pytest.mark.views
def test_default():
    """Create Reserve view instance with default attributes."""
    reserve_view = ReserveTelegramView()
    assert reserve_view.strings == ReserveTelegramStrings


@pytest.mark.reserve
@pytest.mark.telegram
@pytest.mark.views
def test_creation():
    """Create Reserve view instance with specified strings"""
    reserve_view = ReserveTelegramView(RuReserveTelegramStrings)
    assert reserve_view.strings == RuReserveTelegramStrings


@pytest.mark.reserve
@pytest.mark.telegram
@pytest.mark.views
@pytest.mark.eng
def test_create_hello_text_eng():
    """Create reservation main menu message"""
    reserve_view = ReserveTelegramView(RuReserveTelegramStrings)
    assert (reserve_view.create_hello_text() ==
            RuReserveTelegramStrings.hello_message)


@pytest.mark.reserve
@pytest.mark.telegram
@pytest.mark.views
@pytest.mark.ru
def test_create_hello_text_ru():
    """Create reservation main menu message Russian"""
    reserve_view = ReserveTelegramView(RuReserveTelegramStrings)
    assert (reserve_view.create_hello_text() ==
            RuReserveTelegramStrings.hello_message)
