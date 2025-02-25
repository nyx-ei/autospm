import pytest
import jwt
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from user.dependencies import get_current_user
from user.validators import pwd_context, Credentials, UserValidation
from user.models import User
from config import SECRET_TOKEN, TOKEN_ALGORITHM

# Set up the test client
client = TestClient(app)

# Set up of the database for testing
URL_DATABASE = "postgresql://postgres:admin@localhost:5432/testing"
engine = create_engine(URL_DATABASE, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


# Dependency to override get_db dependency of database.py
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)


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


def test_create_user():
    """Testing the creation of a user"""
    response = client.post(
        '/user_registration',
        json={
            "username": "Mart",
            "email": "user@example.com",
            "password": "Stringst12@",
            "name": "string",
            "firstname": "string",
            "date_of_birth": "2025-01-29",
            "phone_number": "+237699245729",
            "address": "string"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data['user']['username'] == "Mart"
    assert data['user']['email'] == "user@example.com"
    assert pwd_context.verify('Stringst12@', data['user']['password'])
    assert data['user']['name'] == "string"
    assert data['user']['firstname'] == "string"
    assert data['user']['date_of_birth'] == "2025-01-29"
    assert data['user']['phone_number'] == "+237699245729"
    assert data['user']['address'] == "string"
    assert 'token' in data


@pytest.mark.asyncio
async def test_login_for_access_token_success(user, credentials):
    token = "access_token"
    otp_code = "123456"

    # Mock the authenticate_user function to return the user
    with patch("user.dependencies.authenticate_user", return_value=user):
        # Mock the create_access_token function to return a token
        with patch("user.utils.create_access_token", return_value=token):
            # Mock the pyotp.TOTP.now method to return an OTP code
            with patch("user.dependencies.pyotp.TOTP.now", return_value=otp_code):
                # Mock the send_email function
                with patch("user.utils.send_email", return_value=None):
                    response = client.post("/token", data={"username": "Mart", "password": "Stringst12@"})

                    assert response.status_code == 200
                    response_data = response.json()
                    assert response_data['token_type'] == 'bearer'

                    # Verify the access token
                    decoded_token = jwt.decode(response_data['access_token'], SECRET_TOKEN,
                                               algorithms=[TOKEN_ALGORITHM])
                    assert decoded_token['username'] == user.username


# Override the get_current_user dependency
@pytest.fixture
def override_get_current_user():
    async def mock_get_current_user():
        return UserValidation(
            username="Mart",
            email="user@example.com",
            password="Stringst12@",
            name="string",
            firstname="string",
            date_of_birth="2025-01-29",
            phone_number="+237699245729",
            address="string"
        )

    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides[get_current_user] = get_current_user


# Test function
def test_read_user(override_get_current_user):
    response = client.get('/login')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['username'] == "Mart"
    assert response_data['email'] == "user@example.com"
    assert response_data['name'] == "string"
    assert response_data['firstname'] == "string"
    assert response_data['date_of_birth'] == "2025-01-29"
    assert response_data['phone_number'] == "+237699245729"
    assert response_data['address'] == "string"

    db = TestingSessionLocal()
    a_user = db.query(User).filter(User.username == 'Mart').first()
    db.delete(a_user)
    db.commit()
    db.close()


@pytest.fixture
def override_get_current_user_unsuccessful():
    async def mock_get_current_user():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides[get_current_user] = get_current_user


def test_read_user_unsuccessful(override_get_current_user_unsuccessful):
    response = client.get('/login')
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
