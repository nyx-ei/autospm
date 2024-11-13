from passlib.context import CryptContext
import jwt
import config
from models_validators.models import User
from fastapi import HTTPException, status
from db.database import SessionLocal


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


async def verify_token(token: str):
    db = SessionLocal()
    try:
        payload = jwt.decode(token, config.SECRET_TOKEN, algorithms=config.TOKEN_ALGORITHM)
        user = db.query(User).filter(User.username == payload['username']).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {'user': user, 'session': db}
