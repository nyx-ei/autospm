from secrets import token_hex
from fastapi_mail import ConnectionConfig
from dotenv import dotenv_values
import os

config_credentials = dotenv_values(os.environ["ENV_PATH"])

SECRET_TOKEN = token_hex(25)
TOKEN_ALGORITHM = config_credentials["TOKEN_ALGORITHM"]

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials['MAIL'],
    MAIL_PASSWORD=config_credentials["PASSWORD"],
    MAIL_FROM=config_credentials["MAIL"],
    MAIL_PORT=config_credentials["MAIL_PORT"],
    MAIL_SERVER=config_credentials["MAIL_SERVER"],
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)

