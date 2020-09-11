import datetime

from copy import deepcopy
from wakebot.entities import Wake, User


def test_wake_default():
    """Create Wake instance with default attributes."""
    wake = Wake()
    assert wake.id is None
    assert wake.user is None
    assert wake.start_date == datetime.date.today()
    assert wake.start_time is None
    assert wake.end is None
    assert wake.end_date is None
    assert wake.end_time is None
    assert wake.count == 1
    assert wake.set_type.set_id == "set"
    assert wake.set_type.minutes == 10
    assert wake.set_count == 1
    assert wake.is_complete is False
    assert wake.canceled is False
    assert wake.cancel_telegram_id is None


def test_wake_creation():
    """Create Wake instance with default attributes."""
    user = User("Firstname")
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=2)

    wake = Wake(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, id=4, board=4, hydro=5,
        canceled=True, cancel_telegram_id=321)
    assert wake.id == 4
    assert wake.user == user
    assert wake.start_date == start.date()
    assert wake.start_time == start.time()
    assert wake.end == end
    assert wake.end_date == end.date()
    assert wake.end_time == end.time()
    assert wake.count == 1
    assert wake.set_type.set_id == "hour"
    assert wake.set_type.minutes == 60
    assert wake.set_count == 2
    assert wake.board == 4
    assert wake.hydro == 5
    assert wake.is_complete is False
    assert wake.canceled is True
    assert wake.cancel_telegram_id == 321
    assert wake.__repr__() == (
        f"Wake(start_date={start.date()!r}, "
        f"start_time={start.time()!r}, set_type='hour', "
        f"set_count=2, minutes=120, board=4, hydro=5, "
        f"is_complete=False)")


def test_wake_comparation():
    """
    Compare Wake instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    wake1 = Wake(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, id=4, board=4, hydro=5,
        canceled=True, cancel_telegram_id=321)

    wake2 = deepcopy(wake1)
    assert wake1 == wake2

    wake2 = deepcopy(wake1)
    wake2.id = 4
    assert wake1 == wake2

    wake2 = deepcopy(wake1)
    wake2.canceled = False
    assert wake1 == wake2

    wake2 = deepcopy(wake1)
    wake2.count = 2
    assert not (wake1 == wake2)

    wake2 = deepcopy(wake1)
    wake2.set_count = 3
    assert not (wake1 == wake2)

    wake2 = deepcopy(wake1)
    wake2.start = wake2.start + datetime.timedelta(minutes=1)
    assert not (wake1 == wake2)

    wake2 = deepcopy(wake1)
    wake2.board = 2
    assert not (wake1 == wake2)

    wake2 = deepcopy(wake1)
    wake2.hydro = 1
    assert not (wake1 == wake2)


def test_wake_copy():
    """
    Copy Wake instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    wake1 = Wake(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, id=4, board=4, hydro=5,
        canceled=True, cancel_telegram_id=321)

    wake2 = deepcopy(wake1)

    assert wake1 == wake2

    wake2.hydro = 2
    assert not (wake1 == wake2)


def test_wake_complete():
    """
    Test Reservation complete attribute
    """
    wake = Wake()
    assert wake.is_complete is False

    wake.start_time = datetime.time(hour=9, minute=10)
    assert wake.is_complete is False

    wake.user = User("Firstname")
    assert wake.is_complete is False

    wake.user.phone_number = "+71234567890"
    assert wake.is_complete is True
