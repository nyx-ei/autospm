import re
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from datetime import date, datetime


class UserValidation(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    firstname: str
    date_of_birth: date
    phone_number: str
    address: str

    def check_valid_pwd(self):
        pwd = self.password
        if len(pwd) < 8:
            raise HTTPException(
                status_code=403,
                detail="Password must contain at least 8 characters."
            )
        if not re.search(r'[A-Z]', pwd):
            raise HTTPException(status_code=403, detail="Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', pwd):
            raise HTTPException(status_code=403, detail="Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', pwd):
            raise HTTPException(status_code=403, detail="Password must contain at least one digit.")
        if not re.search(r'[\W_]', pwd):
            raise HTTPException(status_code=403, detail="Password must contain at least one special character.")
        return pwd

    def check_valid_phone_number(self):
        if not re.match(r"\+2376[25789][0-9]{7}$", self.phone_number):
            raise HTTPException(status_code=403,
                                detail="Phone number should be in in this form: +2376 followed by 2 "
                                       "or 5 or 7 or 8 or 9 and with any 7 digits"
                                )


class Captcha(BaseModel):
    captcha_id: int
    captcha_text: str
    captcha_image: bytes
    created_at: datetime
    expired_at: datetime
