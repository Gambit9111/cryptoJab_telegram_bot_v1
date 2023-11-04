import stripe

import os
from dotenv import load_dotenv
load_dotenv()

# initialize variables
stripe.api_key = os.getenv("STRIPE_API_KEY")
stripe_sub_30_days = os.getenv("STRIPE_SUB_30_DAYS")
stripe_sub_90_days = os.getenv("STRIPE_SUB_90_DAYS")
stripe_sub_365_days = os.getenv("STRIPE_SUB_365_DAYS")
stripe_checkout_success_url = os.getenv("STRIPE_CHECKOUT_SUCCESS_URL")
stripe_checkout_cancel_url = os.getenv("STRIPE_CHECKOUT_CANCEL_URL")


def create_stripe_checkout_session(user_telegram_id: str, product_id: int):

    stripe_sub_duration = None

    # match product_id with stripe_product_id
    match product_id:
        case 0:
            stripe_sub_duration = stripe_sub_30_days
        case 1:
            stripe_sub_duration = stripe_sub_90_days
        case 2:
            stripe_sub_duration = stripe_sub_365_days

    stripe_checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': stripe_sub_duration,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=stripe_checkout_success_url,
        cancel_url=stripe_checkout_cancel_url,
        metadata={'telegram_id': user_telegram_id},
        subscription_data={
            'metadata': {
                'telegram_id': user_telegram_id
            }
        }
    )

    return stripe_checkout_session["url"]