import pytest

from datetime import date, time
from wakebot.entities import Reserve, User
from wakebot.views import ReserveTelegramView
from wakebot.views import ReserveTelegramStringsRu


@pytest.fixture
def reserve():
    user = User(
        firstname="Firstname", lastname="Lastname", middlename="Middlename",
        phone_number="+71234567890", telegram_id=12345, user_id=1,
        is_admin=True)
    reserve = Reserve(
        user=user, start_date=date(2020, 7, 16), start_time=time(17, 20),
        set_type_id="hour", set_count=2, id=4,
        canceled=True, cancel_telegram_id=321)

    return reserve


def test_creation():
    """Create Reserve view instance with specified strings"""
    reserve_view = ReserveTelegramView(ReserveTelegramStringsRu)
    assert reserve_view.strings == ReserveTelegramStringsRu


def test_create_hello_text():
    """Create reservation main menu message"""
    expected_text = "Главное меню сервиса бронирований"
    reserve_view = ReserveTelegramView(ReserveTelegramStringsRu)
    assert (reserve_view.create_hello_text() ==
            expected_text)


def test_get_reservation_info_without_contact(reserve):
    """
    get_reservation_info(<reservation>) method must return
    reservation information without contact data
    """
    reserve_view = ReserveTelegramView(ReserveTelegramStringsRu)

    expected_text = (
        "*Услуга:* Бронирование\n"
        "*Дата:* 16.07.2020\n"
        "*Время начала:* 17:20\n"
        "*Время окончания:* 19:20\n"
        "*Сет:* Час (2)\n"
        "*Количество:* 1"
    )

    actual_text = reserve_view.create_booking_info(reserve=reserve)
    assert actual_text == expected_text


def test_get_reservation_info_full(reserve):
    """
    get_reservation_info(<reservation>, True) method must return
    full reservation information (with contact data)
    """
    reserve_view = ReserveTelegramView(ReserveTelegramStringsRu)
    expected_text = """*Услуга:* Бронирование
*Дата:* 16.07.2020
*Время начала:* 17:20
*Время окончания:* 19:20
*Сет:* Час (2)
*Количество:* 1
"""
    text = reserve_view.create_booking_info(reserve=reserve)
    assert text == expected_text

# Show a booking status without contact information
    expected_text = """*Услуга:* Бронирование
*Имя:* Lastname Firstname Middlename
*Телефон:* +71234567890
*Дата:* 16.07.2020
*Время начала:* 17:20
*Время окончания:* 19:20
*Сет:* Час (2)
*Количество:* 1
"""
    actual_text = reserve_view.create_booking_info(reserve=reserve,
                                                   show_contact=True)
    assert actual_text == expected_text
