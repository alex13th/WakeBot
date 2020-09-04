import pytest
from wakebot.entities import User


@pytest.mark.user
@pytest.mark.entities
@pytest.mark.default
def test_user_default():
    """Create User instance with default attributes."""
    user = User("Firstname")
    assert user.firstname == "Firstname"
    assert user.middlename is None
    assert user.lastname is None
    assert user.displayname == "Firstname"
    assert user.phone_number is None
    assert user.telegram_id is None
    assert user.user_id is None
    assert user.is_admin is False


@pytest.mark.user
@pytest.mark.entities
@pytest.mark.create
def test_user_creation():
    """Create User instance with attributes."""
    user = User(
        firstname="Firstname", lastname="Lastname", middlename="Middlename",
        phone_number="+71234567890", telegram_id=12345, user_id=1,
        is_admin=True)
    assert user.firstname == "Firstname"
    assert user.middlename == "Middlename"
    assert user.lastname == "Lastname"
    assert user.displayname == "Lastname Firstname Middlename"
    assert user.phone_number == "+71234567890"
    assert user.telegram_id == 12345
    assert user.user_id == 1
    assert user.is_admin is True


@pytest.mark.user
@pytest.mark.entities
@pytest.mark.compare
def test_user_comparation():
    """
    Compare User instances.
    """
    user1 = User(
        firstname="Firstname", lastname="Lastname", middlename="Middlename",
        phone_number="+71234567890", telegram_id=12345, user_id=1,
        is_admin=True)

    user2 = User(
        firstname="Firstname", lastname="Lastname", middlename="Middlename",
        phone_number="+71234567890", telegram_id=12345, user_id=1,
        is_admin=True)

    assert user1 == user2

    user2.user_id = 2
    assert user1 == user2

    user2.telegram_id = 54321
    assert not (user1 == user2)
