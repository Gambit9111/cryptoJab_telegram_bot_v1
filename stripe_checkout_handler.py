import stripe

import os
from dotenv import load_dotenv
load_dotenv()

# initialize variables
stripe.api_key = os.getenv("STRIPE_API_KEY")

# ? Product 1 30 days | 45 USD
PRODUCT_1_DURATION = os.getenv("PRODUCT_1_DURATION")
STRIPE_PRODUCT_1_ID = os.getenv("STRIPE_PRODUCT_1_ID")

# ? Product 2 90 days | 120 USD
PRODUCT_2_DURATION = os.getenv("PRODUCT_2_DURATION")
STRIPE_PRODUCT_2_ID = os.getenv("STRIPE_PRODUCT_2_ID")

# ? Product 3 365 days | 360 USD
PRODUCT_3_DURATION = os.getenv("PRODUCT_3_DURATION")
STRIPE_PRODUCT_3_ID = os.getenv("STRIPE_PRODUCT_3_ID")

STRIPE_CHECKOUT_SUCCESS_URL = os.getenv("STRIPE_CHECKOUT_SUCCESS_URL")
STRIPE_CHECKOUT_CANCEL_URL = os.getenv("STRIPE_CHECKOUT_CANCEL_URL")


def create_stripe_checkout_session(user_telegram_id: str, product_id: int):

    selected_stripe_product_id = None
    selected_stripe_product_duration = None

    # match product_id from callback with stripe_product_id
    match product_id:
        case 0:
            selected_stripe_product_duration = PRODUCT_1_DURATION
            selected_stripe_product_id = STRIPE_PRODUCT_1_ID
        case 1:
            selected_stripe_product_duration = PRODUCT_2_DURATION
            selected_stripe_product_id = STRIPE_PRODUCT_2_ID
        case 2:
            selected_stripe_product_duration = PRODUCT_3_DURATION
            selected_stripe_product_id = STRIPE_PRODUCT_3_ID

    stripe_checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': selected_stripe_product_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=STRIPE_CHECKOUT_SUCCESS_URL,
        cancel_url=STRIPE_CHECKOUT_CANCEL_URL,
        metadata={'telegram_id': user_telegram_id, 'duration': selected_stripe_product_duration},
        subscription_data={
            'metadata': {
                'telegram_id': user_telegram_id,
                'duration': selected_stripe_product_duration
            }
        }
    )

    return stripe_checkout_session["url"]