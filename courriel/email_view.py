from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import dotenv_values
from typing import List
from models_validators.models import User
import config
import jwt
import os

config_credentials = dotenv_values(os.environ["ENV_PATH"])
conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials['MAIL'],
    MAIL_PASSWORD=config_credentials["PASSWORD"],
    MAIL_FROM=config_credentials["MAIL"],
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)


async def send_email(email: List, instance: User):
    token_data = {
        "username": instance.username,
        "name": instance.name
    }
    token = jwt.encode(token_data, config.SECRET_TOKEN, config.TOKEN_ALGORITHM)
    template = f"""
        <!DOCTYPE html>
        <html>
            <head></head>
            <body>
                <div style="display: flex; align-items: center; justify-content:center;
                flex-direction: column">
                <h3>Account verification</h3>
                <br>
                <p>Thanks for choosing our website. Please click on the link below to
                to verify your account!
                </p>
                <a style="margin-top: 1rem; padding: 1rem; border-raduis: 0.5rem;
                font-size: 1rem; text-decoration: none; background: #0275d8;
                color: white;" href="http://localhost:8000/verification/?token={token}">Verify your email</a>
            </body> 
        </html>
    """

    message = MessageSchema(
        subject="Account Verification",
        recipients=email,
        body=template,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)
