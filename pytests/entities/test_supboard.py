import datetime
import pytest

from copy import deepcopy
from wakebot.entities import Supboard, User


@pytest.mark.supboard
@pytest.mark.entities
@pytest.mark.default
def test_supboard_default():
    """Create Supboard instance with default attributes."""
    supboard = Supboard()
    assert supboard.id is None
    assert supboard.user is None
    assert supboard.start_date == datetime.date.today()
    assert supboard.start_time is None
    assert supboard.end is None
    assert supboard.end_date is None
    assert supboard.end_time is None
    assert supboard.count == 1
    assert supboard.set_type.set_id == "set"
    assert supboard.set_type.minutes == 30
    assert supboard.set_count == 1
    assert supboard.is_complete is False
    assert supboard.canceled is False
    assert supboard.cancel_telegram_id is None


@pytest.mark.supboard
@pytest.mark.entities
def test_supboard_creation():
    """Create Supboard instance with default attributes."""
    user = User("Firstname")
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=2)

    supboard = Supboard(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, count=3, id=4, canceled=True,
        cancel_telegram_id=321)
    assert supboard.id == 4
    assert supboard.user == user
    assert supboard.start_date == start.date()
    assert supboard.start_time == start.time()
    assert supboard.end == end
    assert supboard.end_date == end.date()
    assert supboard.end_time == end.time()
    assert supboard.count == 3
    assert supboard.set_type.set_id == "hour"
    assert supboard.set_type.minutes == 60
    assert supboard.set_count == 2
    assert supboard.is_complete is False
    assert supboard.canceled is True
    assert supboard.cancel_telegram_id == 321


@pytest.mark.supboard
@pytest.mark.entities
def test_supboard_copy():
    """
    Copy Supboard instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    supboard1 = Supboard(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, id=4,
        canceled=True, cancel_telegram_id=321)

    supboard2 = deepcopy(supboard1)

    assert supboard1 == supboard2

    supboard2.set_count = 3
    assert not (supboard1 == supboard2)


@pytest.mark.supboard
@pytest.mark.entities
def test_supboard_comparation():
    """
    Compare Supboard instances.
    """
    user = User("Firstname")
    start = datetime.datetime.now()

    supboard1 = Supboard(
        user=user, start_date=start.date(), start_time=start.time(),
        set_type_id="hour", set_count=2, count=3, id=4, canceled=True,
        cancel_telegram_id=321)

    supboard2 = deepcopy(supboard1)
    assert supboard1 == supboard2

    supboard2 = deepcopy(supboard1)
    supboard2.id = 4
    assert supboard1 == supboard2

    supboard2 = deepcopy(supboard1)
    supboard2.canceled = False
    assert supboard1 == supboard2

    supboard2 = deepcopy(supboard1)
    supboard2.count = 2
    assert not (supboard1 == supboard2)

    supboard2 = deepcopy(supboard1)
    supboard2.set_count = 3
    assert not (supboard1 == supboard2)

    supboard2 = deepcopy(supboard1)
    supboard2.start = supboard2.start + datetime.timedelta(minutes=1)
    assert not (supboard1 == supboard2)


@pytest.mark.supboard
@pytest.mark.entities
def test_supboard_complete():
    """
    Test Reservation complete attribute
    """
    supboard = Supboard()
    assert supboard.is_complete is False

    supboard.start_time = datetime.time(hour=9, minute=10)
    assert supboard.is_complete is False

    supboard.user = User("Firstname")
    assert supboard.is_complete is False

    supboard.user.phone_number = "+71234567890"
    assert supboard.is_complete is True
