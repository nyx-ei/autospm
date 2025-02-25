from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from typing import List
from datetime import timedelta, datetime
import config
import jwt


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp_time_token': expire.isoformat()})
    token = jwt.encode(to_encode, config.SECRET_TOKEN, config.TOKEN_ALGORITHM)
    return token


async def send_email(email: List, body_msg: str, message_data: str, subject: str):
    template = body_msg.format(message_data)

    message = MessageSchema(
        subject=subject,
        recipients=email,
        body=template,
        subtype=MessageType.html
    )

    fm = FastMail(config.conf)
    try:
        await fm.send_message(message=message)
    except ConnectionErrors as e:
        raise HTTPException(status_code=500, detail=str(e))
