from secrets import token_hex
from fastapi_mail import ConnectionConfig
from dotenv import dotenv_values
import os

SECRET_TOKEN = token_hex(25)
TOKEN_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
VERIFICATION_MSG = """
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
                color: white;" href="http://localhost:8000/verification/?token={}">Verify your email</a>
            </body> 
        </html>
    """

OTP_MSG = """
        <!DOCTYPE html>
        <html>
            <head></head>
            <body>
                <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                  <div style="margin:50px auto;width:70%;padding:20px 0">
                    <div style="border-bottom:1px solid #eee">
                      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
                    </div>
                    <p style="font-size:1.1em">Hi,</p>
                    <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
                    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{}</h2>
                    <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
                    <hr style="border:none;border-top:1px solid #eee" />
                    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                      <p>Your Brand Inc</p>
                      <p>1600 Amphitheatre Parkway</p>
                      <p>California</p>
                    </div>
                  </div>
                </div>
            </body> 
        </html>
    """

VERIFICATION_EMAIL_SUBJECT = "Account Verification"
OTP_EMAIL_SUBJECT = "Your OTP Verification Code"
