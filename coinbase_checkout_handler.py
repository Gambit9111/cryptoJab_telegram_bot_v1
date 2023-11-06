from coinbase_commerce.client import Client

import os
from dotenv import load_dotenv
load_dotenv()

# initialize variables
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")

# ? 30 Days | 0.15 USD
PRODUCT_1_DURATION = os.getenv("PRODUCT_1_DURATION")
COINBASE_PRODUCT_1_PRICE = os.getenv("COINBASE_PRODUCT_1_PRICE")

# ? 90 Days | 0.2 USD
PRODUCT_2_DURATION = os.getenv("PRODUCT_2_DURATION")
COINBASE_PRODUCT_2_PRICE = os.getenv("COINBASE_PRODUCT_2_PRICE")

# ? 365 Days | 0.25 USD
PRODUCT_3_DURATION = os.getenv("PRODUCT_3_DURATION")
COINBASE_PRODUCT_3_PRICE = os.getenv("COINBASE_PRODUCT_3_PRICE")

coinbase_base_url = "https://commerce.coinbase.com/checkout/"
coinbase_client = Client(api_key=COINBASE_API_KEY)

def create_coinbase_checkout_session(user_telegram_id: str, product_id: int):

    selected_coinbase_product_price = None
    selected_coinbase_product_duration = None

    # match product_id with coinbase_product_id
    match product_id:
        case 0:
            # ? 30 days
            selected_coinbase_product_price = COINBASE_PRODUCT_1_PRICE
            selected_coinbase_product_duration = PRODUCT_1_DURATION
        case 1:
            # ? 90 days
            selected_coinbase_product_price = COINBASE_PRODUCT_2_PRICE
            selected_coinbase_product_duration = PRODUCT_2_DURATION
        case 2:
            # ? 365 days
            selected_coinbase_product_price = COINBASE_PRODUCT_3_PRICE
            selected_coinbase_product_duration = PRODUCT_3_DURATION
    
    coinbase_checkout_info = {
        "name": f"Subscription for {selected_coinbase_product_duration} days",
        "description": user_telegram_id,
        "local_price": {
            "amount": selected_coinbase_product_price,
            "currency": "USD"
        },
        "pricing_type": "fixed_price",
        "requested_info": ["email"]
    }

    coinbase_checkout_session = coinbase_client.checkout.create(**coinbase_checkout_info)

    return coinbase_base_url + coinbase_checkout_session["id"]