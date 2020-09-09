import datetime
import pytest

from copy import deepcopy
from wakebot.entities import Bathhouse, User


@pytest.mark.bathhouse
@pytest.mark.entities
@pytest.mark.default
def test_bathhouse_default():
    """Create Bathhouse instance with default attributes."""
    bathhouse = Bathhouse()
    assert bathhouse.id is None
    assert bathhouse.user is None
    assert bathhouse.start_date == datetime.date.today()
    assert bathhouse.start_time is None
    assert bathhouse.end is None
    assert bathhouse.end_date is None
    assert bathhouse.end_time is None
    assert bathhouse.count == 1
    assert bathhouse.set_type.set_id == "hour"
    assert bathhouse.set_type.minutes == 60
    assert bathhouse.set_count == 1
    assert bathhouse.is_complete is False
    assert bathhouse.canceled is False
    assert bathhouse.cancel_telegram_id is None


@pytest.mark.bathhouse
@pytest.mark.entities
def test_bathhouse_creation():
    """Create Bathhouse instance with default attributes."""
    user = User("Firstname")
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=1)

    bathhouse = Bathhouse(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="set", set_count=2, count=3, id=4, canceled=True,
        cancel_telegram_id=321)
    assert bathhouse.id == 4
    assert bathhouse.user == user
    assert bathhouse.start_date == start.date()
    assert bathhouse.start_time == start.time()
    assert bathhouse.end == end
    assert bathhouse.end_date == end.date()
    assert bathhouse.end_time == end.time()
    assert bathhouse.count == 3
    assert bathhouse.set_type.set_id == "set"
    assert bathhouse.set_type.minutes == 30
    assert bathhouse.set_count == 2
    assert bathhouse.is_complete is True  # Don't require a phone number
    assert bathhouse.canceled is True
    assert bathhouse.cancel_telegram_id == 321
    assert bathhouse.__repr__() == (
        f"Bathhouse(start_date={start.date()!r}, "
        f"start_time={start.time()!r}, set_type='set', "
        f"set_count=2, minutes=60, is_complete=True)")

@pytest.mark.bathhouse
@pytest.mark.entities
def test_bathhouse_copy():
    """
    Copy Bathhouse instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    bathhouse1 = Bathhouse(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, id=4,
        canceled=True, cancel_telegram_id=321)

    bathhouse2 = deepcopy(bathhouse1)

    assert bathhouse1 == bathhouse2

    bathhouse2.set_count = 3
    assert not (bathhouse1 == bathhouse2)


@pytest.mark.bathhouse
@pytest.mark.entities
def test_bathhouse_comparation():
    """
    Compare Bathhouse instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    bathhouse1 = Bathhouse(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, count=3, id=4, canceled=True,
        cancel_telegram_id=321)

    bathhouse2 = deepcopy(bathhouse1)
    assert bathhouse1 == bathhouse2

    bathhouse2 = deepcopy(bathhouse1)
    bathhouse2.id = 4
    assert bathhouse1 == bathhouse2

    bathhouse2 = deepcopy(bathhouse1)
    bathhouse2.canceled = False
    assert bathhouse1 == bathhouse2

    bathhouse2 = deepcopy(bathhouse1)
    bathhouse2.count = 2
    assert not (bathhouse1 == bathhouse2)

    bathhouse2 = deepcopy(bathhouse1)
    bathhouse2.set_count = 3
    assert not (bathhouse1 == bathhouse2)

    bathhouse2 = deepcopy(bathhouse1)
    bathhouse2.start = bathhouse2.start + datetime.timedelta(minutes=1)
    assert not (bathhouse1 == bathhouse2)


@pytest.mark.bathhouse
@pytest.mark.entities
def test_bathhouse_complete():
    """
    Test Reservation complete attribute
    """
    bathhouse = Bathhouse()
    assert bathhouse.is_complete is False

    bathhouse.start_time = datetime.time(hour=9, minute=10)
    assert bathhouse.is_complete is False

    bathhouse.user = User("Firstname")
    assert bathhouse.is_complete is True

    bathhouse.user.phone_number = "+71234567890"
    assert bathhouse.is_complete is True
