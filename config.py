from secrets import token_hex
from fastapi_mail import ConnectionConfig
from dotenv import dotenv_values
import os
SECRET_TOKEN = token_hex(25)
TOKEN_ALGORITHM = 'HS256'

config_credentials = dotenv_values(os.environ["ENV_PATH"])
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

