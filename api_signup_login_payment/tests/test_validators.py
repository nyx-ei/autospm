import pytest
from user.validators import UserValidation, Credentials
from datetime import date
from pydantic import ValidationError


@pytest.fixture
def user() -> UserValidation:
    """Pytest fixture to create a User instance for testing."""
    return UserValidation(
        username="Germinal",
        email="germinal@gmail.com",
        password="Germinal@0099",
        name="Forest",
        firstname="Germs",
        date_of_birth=date(1998, 12, 4),
        phone_number="+237677448877",
        address="Mvog-ada Yaounde"
    )


@pytest.fixture
def cred() -> Credentials:
    """Pytest fixture to create a Credentials instance for testing."""
    return Credentials(
        username="Germinal",
        password="Germinal@0099"
    )


def test_user_validation_creation(user: UserValidation) -> None:
    """Test the creation of user pydantic for validation."""
    assert user.username == "Germinal"
    assert user.email == "germinal@gmail.com"
    assert user.password == "Germinal@0099"
    assert user.name == "Forest"
    assert user.firstname == "Germs"
    assert user.date_of_birth == date(1998, 12, 4)
    assert user.phone_number == "+237677448877"
    assert user.address == "Mvog-ada Yaounde"


def test_missing_field() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            email="germinal@gmail.com",
            password="Germinal@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877"
        )


def test_invalid_field() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username=123,
            email="germinal@gmail.com",
            password="Germinal@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_email_pattern() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username="germinal",
            email="germinalgmail.com",
            password="Germinal@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_password_length_constraint() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username="Germinal",
            email="germinal@gmail.com",
            password="Ge@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_password_pattern_upper_constraint() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username="Germinal",
            email="germinal@gmail.com",
            password="germinal@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_password_pattern_lower_constraint() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username="Germinal",
            email="germinal@gmail.com",
            password="GERMINAL@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_password_pattern_digit() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username="Germinal",
            email="germinal@gmail.com",
            password="Germinal@",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_password_pattern_special_char() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username="Germinal",
            email="germinal@gmail.com",
            password="Germinal123",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+237677448877",
            address="Mvog-ada Yaounde"
        )


def test_phone_length() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username=123,
            email="germinal@gmail.com",
            password="Germinal@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="+23767744887",
            address="Mvog-ada Yaounde"
        )


def test_phone_pattern() -> None:
    with pytest.raises(ValidationError):
        UserValidation(
            username=123,
            email="germinal@gmail.com",
            password="Germinal@0099",
            name="Forest",
            firstname="Germs",
            date_of_birth=date(1998, 12, 4),
            phone_number="677448877",
            address="Mvog-ada Yaounde"
        )
