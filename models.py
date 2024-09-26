import re
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from datetime import date


class User(Model):
    username = fields.CharField(max_length=50, null=False, pk=True, unique=True, index=True)
    email = fields.CharField(max_length=255, null=False, unique=True)
    password = fields.CharField(max_length=255, null=False)
    name = fields.CharField(max_length=255, null=False)
    firstname = fields.CharField(max_length=100)
    date_of_birth = fields.DateField(null=False)
    phone_number = fields.CharField(max_length=20, null=False)
    address = fields.CharField(max_length=255)
    is_verified = fields.BooleanField(default=False)


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


class SubscriptionType(Model):
    id = fields.IntField(pk=True, null=False, unique=True, index=True)
    subscription_name = fields.CharField(max_length=150, null=False, unique=True)
    price = fields.IntField(null=False)


class Subscription(Model):
    username = fields.ForeignKeyField('models.User', related_name='subscription')
    id_subscription_type = fields.ForeignKeyField('models.SubscriptionType', related_name='subscription')
    begin = fields.DatetimeField(null=False)
    end = fields.DatetimeField(null=False)

    class Meta:
        unique_together = (('username', 'id_subscription_type'),)
        primary_key = ('username', 'id_subscription_type')


class Captcha(Model):
    captcha_id = fields.IntField(pk=True, null=False, unique=True, index=True)
    captcha_text = fields.CharField(max_length=6, null=False)
    captcha_image = fields.BinaryField(null=False)
    created_at = fields.DatetimeField(null=False)
    expired_at = fields.DatetimeField(null=False)


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified",))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True, exclude=("is_verified",))
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password",))

subscription_type_pydantic = pydantic_model_creator(SubscriptionType, name="SubscriptionType")
subscription_type_pydanticIn = pydantic_model_creator(SubscriptionType, name="SubscriptionTypeIn",
                                                      exclude_readonly=True)

subscription_pydantic = pydantic_model_creator(Subscription, name="Subscription", exclude=("begin",))
subscription_pydanticIn = pydantic_model_creator(Subscription, name="SubscriptionIn", exclude_readonly=True)

captcha_pydantic = pydantic_model_creator(Captcha, name="Captcha", exclude=("created_at", "expired_at"))
captcha_pydanticIn = pydantic_model_creator(Captcha, name="Captcha", exclude_readonly=True,
                                            exclude=("created_at", "expired_at"))
