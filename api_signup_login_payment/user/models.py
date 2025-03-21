from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from database import Base
from datetime import date


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(primary_key=True, index=True, unique=True)
    email: Mapped[str]
    password: Mapped[str]
    name: Mapped[str]
    firstname: Mapped[str]
    date_of_birth: Mapped[date]
    phone_number: Mapped[str]
    address: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f"This is the user with \nUsername: {self.username} and with the" \
               f"name: {self.name}"


class SubscriptionType(Base):
    __tablename__ = 'subscription_type'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    subscription_name: Mapped[str]
    price: Mapped[int]


class Subscription(Base):
    __tablename__ = 'subscription'
    username: Mapped[str] = mapped_column(ForeignKey("users.username"), primary_key=True)
    id_subscription_type: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), primary_key=True)
    begin: Mapped[date]
    end: Mapped[date]