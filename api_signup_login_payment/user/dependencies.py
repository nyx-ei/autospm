from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt
import pyotp

from user.validators import Credentials
from user.models import User
from database import get_db
import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


#############################################################################
#           HELPERS FUNCTIONS FOR OUR ENDPOINTS                             #
#############################################################################
# This function checks if the user exist
async def get_user(db: Annotated[Session, Depends(get_db)], username: str) -> User:
    return db.scalar(select(User).where(User.username == username))


async def authenticate_user(cred: Credentials, db: Annotated[Session, Depends(get_db)]) -> User or bool:
    user = await get_user(db, cred.username)
    if not user:
        return False
    if not cred.verify_pwd(user.password):
        return False
    return user


def otp_checker(otp: str, otp_secret: str) -> bool:
    curr_otp = pyotp.TOTP(otp_secret, interval=300)
    return curr_otp.verify(otp)


async def verify_token_email(token: str, db: Annotated[Session, Depends(get_db)]):
    try:
        payload = jwt.decode(token, config.SECRET_TOKEN, algorithms=config.TOKEN_ALGORITHM)
        user = db.query(User).filter(User.username == payload['username']).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {'user': user, 'session': db}


async def get_current_user(db: Annotated[Session, Depends(get_db)],
                           token: Annotated[str, Depends(oauth2_scheme)], otp_code: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_TOKEN, algorithms=config.TOKEN_ALGORITHM)
    except jwt.PyJWTError:
        raise credentials_exception
    if not payload['username']:
        raise credentials_exception
    user = await get_user(db, payload['username'])
    if not user:
        raise credentials_exception
    state = otp_checker(otp_code, payload['otp_secret'])
    if state:
        return user
    raise credentials_exception
