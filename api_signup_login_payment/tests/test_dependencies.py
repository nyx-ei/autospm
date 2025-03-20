import pytest
import pyotp
import jwt
from unittest.mock import MagicMock, patch, ANY
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from user.models import User
from user.validators import Credentials
from user.dependencies import verify_token_email, get_user, authenticate_user, otp_checker, get_current_user


@pytest.fixture
def db_session():
    # Set up a test database session
    session = MagicMock(spec=Session)
    yield session


@pytest.fixture
def user() -> User:
    """Pytest fixture to create a User instance for testing."""
    return User(
        username="Mart",
        email="user@example.com",
        password="Stringst12@",
        name="string",
        firstname="string",
        date_of_birth="2025-01-29",
        phone_number="+237699245729",
        address="string"
    )


@pytest.fixture
def credentials():
    cred = MagicMock(spec=Credentials)
    cred.username = "Mart"
    cred.verify_pwd.return_value = True
    yield cred


@pytest.fixture
def token():
    # Set up a mock token
    return "valid_token"


@pytest.fixture
def otp_code():
    # Set up a mock OTP code
    return "123456"


@pytest.mark.asyncio
async def test_verify_token_email_success(db_session, user: User, token):
    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value={"username": "testuser"}):
        # Mock the database query to return a user
        db_session.query.return_value.filter.return_value.first.return_value = user

        result = await verify_token_email(token, db_session)

        assert result['user'] == user
        assert result['session'] == db_session


@pytest.mark.asyncio
async def test_verify_token_email_invalid_token(db_session):
    token = "invalid_token"

    # Mock the jwt.decode function to raise an exception
    with patch("user.dependencies.jwt.decode", side_effect=Exception("Invalid token")):
        with pytest.raises(HTTPException) as exc_info:
            await verify_token_email(token, db_session)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid token"


@pytest.mark.asyncio
async def test_get_user(db_session, user: User):
    """Test the function user.dependencies.get_user"""
    username = "Mart"
    db_session.scalar.return_value = user
    result = await get_user(db_session, username)

    assert result == user
    db_session.scalar.assert_called_once_with(ANY)


@pytest.mark.asyncio
async def test_authenticate_user_success(db_session, credentials):
    user = User(username="Mart", password="hashed_password")

    # Mock the get_user function to return the user
    with patch("user.dependencies.get_user", return_value=user):
        result = await authenticate_user(credentials, db_session)

        assert result == user
        credentials.verify_pwd.assert_called_once_with(user.password)


@pytest.mark.asyncio
async def test_authenticate_user_no_user(db_session, credentials):
    # Mock the get_user function to return None
    with patch("user.dependencies.get_user", return_value=None):
        result = await authenticate_user(credentials, db_session)

        assert result is False


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(db_session, credentials):
    user = User(username="Mart", password="hashed_password")

    # Mock the get_user function to return the user
    with patch("user.dependencies.get_user", return_value=user):
        # Mock the verify_pwd method to return False
        credentials.verify_pwd.return_value = False

        result = await authenticate_user(credentials, db_session)

        assert result is False
        credentials.verify_pwd.assert_called_once_with(user.password)


@pytest.fixture
def otp_secret():
    # Set up a mock OTP secret
    return pyotp.random_base32()


def test_otp_checker_valid_otp(otp_secret):
    # Generate a valid OTP
    totp = pyotp.TOTP(otp_secret, interval=300)
    valid_otp = totp.now()

    result = otp_checker(valid_otp, otp_secret)

    assert result is True


def test_otp_checker_invalid_otp(otp_secret):
    # Generate an invalid OTP
    invalid_otp = "123456"

    result = otp_checker(invalid_otp, otp_secret)

    assert result is False


@pytest.mark.asyncio
async def test_get_current_user_success(db_session, token, otp_code, user: User):
    payload = {"username": "testuser", "otp_secret": "secret"}

    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value=payload):
        # Mock the get_user function to return the user
        with patch("user.dependencies.get_user", return_value=user):
            # Mock the otp_checker function to return True
            with patch("user.dependencies.otp_checker", return_value=True):
                result = await get_current_user(db_session, token, otp_code)

                assert result == user


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_session, otp_code):
    token = "invalid_token"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Mock the jwt.decode function to raise an exception
    with patch("user.dependencies.jwt.decode", side_effect=jwt.PyJWTError):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(db_session, token, otp_code)

        assert exc_info.value.status_code == credentials_exception.status_code
        assert exc_info.value.detail == credentials_exception.detail


@pytest.mark.asyncio
async def test_get_current_user_no_user(db_session, token, otp_code):
    payload = {"username": "Mart", "otp_secret": "secret"}
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value=payload):
        # Mock the get_user function to return None
        with patch("user.dependencies.get_user", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(db_session, token, otp_code)

            assert exc_info.value.status_code == credentials_exception.status_code
            assert exc_info.value.detail == credentials_exception.detail


@pytest.mark.asyncio
async def test_get_current_user_invalid_otp(db_session, token, otp_code, user: User):
    payload = {"username": "Mart", "otp_secret": "secret"}
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value=payload):
        # Mock the get_user function to return the user
        with patch("user.dependencies.get_user", return_value=user):
            # Mock the otp_checker function to return False
            with patch("user.dependencies.otp_checker", return_value=False):
                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(db_session, token, otp_code)

                assert exc_info.value.status_code == credentials_exception.status_code
                assert exc_info.value.detail == credentials_exception.detail


@pytest.mark.asyncio
async def test_get_current_user_success(db_session, token, otp_code, user):
    payload = {"username": "Mart", "otp_secret": "secret"}

    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value=payload):
        # Mock the get_user function to return the user
        with patch("user.dependencies.get_user", return_value=user):
            # Mock the otp_checker function to return True
            with patch("user.dependencies.otp_checker", return_value=True):
                result = await get_current_user(db_session, token, otp_code)

                assert result == user


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_session, otp_code):
    token = "invalid_token"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Mock the jwt.decode function to raise an exception
    with patch("user.dependencies.jwt.decode", side_effect=jwt.PyJWTError):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(db_session, token, otp_code)

        assert exc_info.value.status_code == credentials_exception.status_code
        assert exc_info.value.detail == credentials_exception.detail


@pytest.mark.asyncio
async def test_get_current_user_no_user(db_session, token, otp_code):
    payload = {"username": "testuser", "otp_secret": "secret"}
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value=payload):
        # Mock the get_user function to return None
        with patch("user.dependencies.get_user", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(db_session, token, otp_code)

            assert exc_info.value.status_code == credentials_exception.status_code
            assert exc_info.value.detail == credentials_exception.detail


@pytest.mark.asyncio
async def test_get_current_user_invalid_otp(db_session, token, otp_code):
    user = User(username="testuser")
    payload = {"username": "testuser", "otp_secret": "secret"}
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Mock the jwt.decode function to return a valid payload
    with patch("user.dependencies.jwt.decode", return_value=payload):
        # Mock the get_user function to return the user
        with patch("user.dependencies.get_user", return_value=user):
            # Mock the otp_checker function to return False
            with patch("user.dependencies.otp_checker", return_value=False):
                with pytest.raises(HTTPException) as exc_info:
                    await get_current_user(db_session, token, otp_code)

                assert exc_info.value.status_code == credentials_exception.status_code
                assert exc_info.value.detail == credentials_exception.detail
