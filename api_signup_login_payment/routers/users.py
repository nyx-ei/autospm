from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
import pyotp

from user.validators import UserValidation, Credentials
from user.models import User
from database import get_db
from user.dependencies import verify_token_email, get_user, authenticate_user, get_current_user
from user.utils import send_email, create_access_token
from config import VERIFICATION_EMAIL_SUBJECT, VERIFICATION_MSG, OTP_MSG, OTP_EMAIL_SUBJECT

router = APIRouter()
template = Jinja2Templates(directory="templates")

#############################################################################
#                    ENDPOINTS(ROUTES) FUNCTIONS                            #
#############################################################################

@router.post('/user_registration')
async def create_user(user: UserValidation, db: Annotated[Session, Depends(get_db)]):
    # Here we check if the user is already in the database
    if await get_user(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Creation of an unverified user in the database
    user_obj = User(
        username=user.username,
        email=user.email,
        password=user.hashed_pwd(),
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
    token = await create_access_token(data={'username': user_obj.username})
    await send_email([user_obj.email], VERIFICATION_MSG, token, VERIFICATION_EMAIL_SUBJECT)

    return {
        "status": "Ok",
        "data": f"Hello {user_obj.username}, thanks for choosing our services. Please check your email inbox and "
        f"click on the link to confirm your email"
    }


@router.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str, db: Annotated[Session, Depends(get_db)]):
    result = await verify_token_email(token, db)

    if result['user'] and not result['user'].is_verified:
        result['user'].is_verified = True
        result['session'].commit()
        return template.TemplateResponse("email_verification.html",
                                         {"request": request, "username": result['user'].username})


@router.post('/token')
async def login_for_access_token(db: Annotated[Session, Depends(get_db)],
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(Credentials(username=form_data.username, password=form_data.password), db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    curr_otp_secret = pyotp.random_base32()
    payload = {'username': user.username, 'otp_secret': curr_otp_secret}
    token = await create_access_token(payload)

    otp = pyotp.TOTP(curr_otp_secret, interval=300)
    otp_code = otp.now()
    await send_email([user.email], OTP_MSG, otp_code, OTP_EMAIL_SUBJECT)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/login', response_model=UserValidation)
async def read_user(user: Annotated[User, Depends(get_current_user)]):
    return user
