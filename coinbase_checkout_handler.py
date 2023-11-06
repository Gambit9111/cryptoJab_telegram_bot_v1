from coinbase_commerce.client import Client

import os
from dotenv import load_dotenv
load_dotenv()

# initialize variables
coinbase_api_key = os.getenv("COINBASE_API_KEY")

# ? 30 Days | 0.15 USD
coinbase_sub_option_1_duration = os.getenv("COINBASE_SUB_OPTION_1_DURATION")
coinbase_sub_option_1_price = os.getenv("COINBASE_SUB_OPTION_1_PRICE")

# ? 90 Days | 0.20 USD
coinbase_sub_option_2_duration = os.getenv("COINBASE_SUB_OPTION_2_DURATION")
coinbase_sub_option_2_price = os.getenv("COINBASE_SUB_OPTION_2_PRICE")

# ? 365 Days | 0.25 USD
coinbase_sub_option_3_duration = os.getenv("COINBASE_SUB_OPTION_3_DURATION")
coinbase_sub_option_3_price = os.getenv("COINBASE_SUB_OPTION_3_PRICE")

coinbase_base_url = "https://commerce.coinbase.com/checkout/"
coinbase_client = Client(api_key=coinbase_api_key)

def create_coinbase_checkout_session(user_telegram_id: str, product_id: int):

    coinbase_sub_duration = None
    coinbase_sub_price = None

    # match product_id with coinbase_product_id
    match product_id:
        case 0:
            # ? 30 days
            coinbase_sub_duration = coinbase_sub_option_1_duration
            coinbase_sub_price = coinbase_sub_option_1_price
        case 1:
            # ? 90 days
            coinbase_sub_duration = coinbase_sub_option_2_duration
            coinbase_sub_price = coinbase_sub_option_2_price
        case 2:
            # ? 365 days
            coinbase_sub_duration = coinbase_sub_option_3_duration
            coinbase_sub_price = coinbase_sub_option_3_price
    
    coinbase_checkout_info = {
        "name": f"Subscription for {coinbase_sub_duration} days",
        "description": user_telegram_id,
        "local_price": {
            "amount": coinbase_sub_price,
            "currency": "USD"
        },
        "pricing_type": "fixed_price",
        "requested_info": ["email"]
    }

    coinbase_checkout_session = coinbase_client.checkout.create(**coinbase_checkout_info)

    return coinbase_base_url + coinbase_checkout_session["id"]