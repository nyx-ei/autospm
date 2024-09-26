from passlib.context import CryptContext
import jwt
import config
from models import User
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hashed_password(password):
    return pwd_context.hash(password)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_TOKEN, config.TOKEN_ALGORITHM)
        user = await User.get(username=payload.get("username"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user
