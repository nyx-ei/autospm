from fastapi import FastAPI, HTTPException, status, Request
from tortoise import models
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import get_hashed_password, verify_token
from fastapi.responses import HTMLResponse
from email_view import send_email

app = FastAPI()


@app.get('/')
def index():
    return {"message": "Hellooooo"}

# Route to register a user.
@app.post('/registration')
async def create_user(user: UserValidation):
    # Check if the user exist
    if await User.get_or_none(username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username: {user.username} already exists."
        )

    # Validate password and phone number fields
    user.check_valid_pwd()
    user.check_valid_phone_number()

    # Creation of an unverified user in the database
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)

    # Send confirmation email
    await send_email([user_obj.email], user_obj)

    return {
        "status": "Ok",
        "data": f"Hello {new_user.username}, thanks for choosing our services. Please check your email inbox and "
                f"click on the link to confirm your email"
    }


@app.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
register_tortoise(
    app,
    db_url="postgres://postgres:admin@localhost:5432/autopm_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
