from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse
from models_validators.models import User
from models_validators.validators import UserValidation
from courriel.email_auth import get_hashed_password, verify_token

from courriel.email_view import send_email
from db.database import SessionLocal, engine, Base
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
# templates
from fastapi.templating import Jinja2Templates

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/')
def index():
    return {"message": "Hellooooo"}


# Route to register a user.
@app.post('/registration')
async def create_user(user: UserValidation, db: db_dependency):
    # Check if the user exist
    if db.scalar(select(User).where(User.username == user.username)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username: {user.username} already exists."
        )

    # Validate password and phone number fields
    user.check_valid_pwd()
    user.check_valid_phone_number()

    # Creation of an unverified user in the database
    user_obj = User(
        username=user.username,
        email=user.email,
        password=get_hashed_password(user.password),
        name=user.name,
        firstname=user.firstname,
        date_of_birth=user.date_of_birth,
        phone_number=user.phone_number,
        address=user.address,
        is_verified=False
    )
    db.add(user_obj)
    db.commit()

    # Send confirmation email
    await send_email([user_obj.email], user_obj)

    return {
        "status": "Ok",
        "data": f"Hello {user_obj.username}, thanks for choosing our services. Please check your email inbox and "
                f"click on the link to confirm your email"
    }


template = Jinja2Templates(directory="templates")


@app.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    result = await verify_token(token)

    if result['user'] and not result['user'].is_verified:
        result['user'].is_verified = True
        result['session'].commit()
        return template.TemplateResponse("email_verification.html",
                                         {"request": request, "username": result['user'].username})
