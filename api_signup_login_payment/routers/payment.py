import os
import json
import stripe
from datetime import datetime
from fastapi import APIRouter, Header, HTTPException, status, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated
from sqlalchemy.orm import Session

from user.dependencies import get_user_with_email
from user.models import Subscription
from database import get_db

router = APIRouter()
template = Jinja2Templates(directory="templates")

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

stripe.api_key = os.getenv('STRIPE_KEY')
webhook_secret = os.getenv('WEBHOOK_SECRET')
DOMAIN_NAME = os.getenv('DOMAIN')


@router.post('/payment-stripe-checkout-session')
async def create_stripe_checkout_session(price_id: str, user_email: str, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to create a checkout session
    it takes 3 arguments:
        --> price_id of the stripe product
        --> user_email: This parameter is very important for us to know which user did the payment
                        since a user can use somebody's card to pay.
        --> db: Here we are using a session of a database to identify the user.

    This function returns the payment link.
    """
    if not await get_user_with_email(db, user_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exit"
        )
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=user_email,
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=DOMAIN_NAME + '/success',
            cancel_url=DOMAIN_NAME + '/cancel',
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return {'payment_link': checkout_session['url']}


@router.get('/success', response_class=HTMLResponse)
def get_success_page(request: Request):
    """Endpoint that retrieves the success page"""
    return template.TemplateResponse('success.html', {"request": request})


@router.get('/cancel', response_class=HTMLResponse)
def get_success_page(request: Request):
    """Endpoint that retrieves the cancel page"""
    return template.TemplateResponse('cancel.html', {"request": request})


@router.post('/webhook')
async def webhook(request: Request, db: Annotated[Session, Depends(get_db)], stripe_signature: str = Header(None)):
    """Endpoint for actions after a payment(or during a payment process):
    here we persist the subscription in the DB"""
    data_bytes = await request.body()

    # Processing to have a dictionary object that will help to have the Subscription object from stripe
    data_bytes_to_str = data_bytes.decode("UTF-8").strip("\n                ")
    data_to_dict = json.loads(data_bytes_to_str)
    try:
        event = stripe.Webhook.construct_event(
            payload=data_bytes,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
    except Exception as e:
        return {'error': str(e)}

    if event['type'] == 'checkout.session.completed':
        user = await get_user_with_email(db, data_to_dict["data"]["object"]["customer_email"])

        # Extract subscription id, start date and end date from the payload
        stripe_subscription_obj = stripe.Subscription.retrieve(data_to_dict["data"]["object"]["subscription"])
        start_date = datetime.utcfromtimestamp(stripe_subscription_obj["current_period_start"])
        end_date = datetime.utcfromtimestamp(stripe_subscription_obj["current_period_end"])

        # Persist subscription in the database
        subscription = Subscription(
            username=user.username,
            id_subscription_type=stripe_subscription_obj["plan"]["product"],
            begin=start_date,
            end=end_date
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    else:
        pass

    return {'status': 'success'}
