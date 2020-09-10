import datetime
import pytest

from copy import deepcopy
from wakebot.entities import Reserve, User


@pytest.mark.reserve
@pytest.mark.entities
@pytest.mark.default
def test_reserve_default():
    """Create Reserve instance with default attributes."""
    reserve = Reserve()
    assert reserve.id is None
    assert reserve.user is None
    assert reserve.start_date == datetime.date.today()
    assert reserve.start_time is None
    assert reserve.end is None
    assert reserve.end_date is None
    assert reserve.end_time is None
    assert reserve.count == 1
    assert reserve.set_type.set_id == "set"
    assert reserve.set_type.minutes == 5
    assert reserve.set_count == 1
    assert reserve.is_complete is False
    assert reserve.canceled is False
    assert reserve.cancel_telegram_id is None


@pytest.mark.reserve
@pytest.mark.entities
def test_reserve_creation():
    """Create Reserve instance with default attributes."""
    user = User("Firstname")
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=2)

    reserve = Reserve(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, count=3, id=4, canceled=True,
        cancel_telegram_id=321)

    assert reserve.id == 4
    assert reserve.user == user
    assert reserve.start_date == start.date()
    assert reserve.start_time == start.time()
    assert reserve.end == end
    assert reserve.end_date == end.date()
    assert reserve.end_time == end.time()
    assert reserve.count == 3
    assert reserve.set_type.set_id == "hour"
    assert reserve.set_type.minutes == 60
    assert reserve.set_count == 2
    assert reserve.is_complete is False
    assert reserve.canceled is True
    assert reserve.cancel_telegram_id == 321
    assert reserve.__repr__() == (
        f"Reservation(start_date={start.date()!r}, "
        f"start_time={start.time()!r}, set_type='hour', "
        f"set_count=2, minutes=120, is_complete=False)")


@pytest.mark.reserve
@pytest.mark.entities
def test_reserve_copy():
    """
    Copy Reserve instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    reserve1 = Reserve(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, id=4,
        canceled=True, cancel_telegram_id=321)

    reserve2 = deepcopy(reserve1)

    assert reserve1 == reserve2

    reserve2.set_count = 3
    assert not (reserve1 == reserve2)


@pytest.mark.reserve
@pytest.mark.entities
def test_reserve_comparation():
    """
    Compare Reserve instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    reserve1 = Reserve(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, count=3, id=4, canceled=True,
        cancel_telegram_id=321)

    reserve2 = deepcopy(reserve1)
    assert reserve1 == reserve2

    reserve2 = deepcopy(reserve1)
    reserve2.id = 4
    assert reserve1 == reserve2

    reserve2 = deepcopy(reserve1)
    reserve2.canceled = False
    assert reserve1 == reserve2

    reserve2 = deepcopy(reserve1)
    reserve2.count = 2
    assert not (reserve1 == reserve2)

    reserve2 = deepcopy(reserve1)
    reserve2.set_count = 3
    assert not (reserve1 == reserve2)

    reserve2 = deepcopy(reserve1)
    reserve2.start = reserve2.start + datetime.timedelta(minutes=1)
    assert not (reserve1 == reserve2)


@pytest.mark.reserve
@pytest.mark.entities
def test_reserve_complete():
    """
    Test Reservation complete attribute
    """
    reserve = Reserve()
    assert reserve.is_complete is False

    reserve.start_time = datetime.time(hour=9, minute=10)
    assert reserve.is_complete is False

    reserve.user = User("Firstname")
    assert reserve.is_complete is False

    reserve.user.phone_number = "+71234567890"
    assert reserve.is_complete is True
