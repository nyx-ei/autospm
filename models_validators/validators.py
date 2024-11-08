import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime


class UserValidation(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)
    name: str
    firstname: str
    date_of_birth: date
    phone_number: str
    address: str

    @field_validator('password')
    def check_valid_pwd(cls, v):
        if not re.match(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).*$", v):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter"
                             "one digit and at least on special character.")
        return v

    
    @field_validator('phone_number')
    def check_valid_phone_number(cls, v):
        if not re.match(r"\+2376[25789][0-9]{7}$", v):
            raise ValueError("Phone number must be in the form +237 follows by 9 digits")
        return v.title()


class Captcha(BaseModel):
    captcha_id: int
    captcha_text: str
    captcha_image: bytes
    created_at: datetime
    expired_at: datetime
