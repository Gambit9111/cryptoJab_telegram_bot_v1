from coinbase_commerce.client import Client

import os
from dotenv import load_dotenv
load_dotenv()

# initialize variables
coinbase_api_key = os.getenv("COINBASE_API_KEY")
coinbase_sub_30_days = os.getenv("COINBASE_SUB_30_DAYS")
coinbase_sub_90_days = os.getenv("COINBASE_SUB_90_DAYS")
coinbase_sub_365_days = os.getenv("COINBASE_SUB_365_DAYS")
coinbase_base_url = "https://commerce.coinbase.com/checkout/"
coinbase_client = Client(api_key=coinbase_api_key)

def create_coinbase_checkout_session(user_telegram_id: str, product_id: int):

    coinbase_sub_duration = None

    # match product_id with coinbase_product_id
    match product_id:
        case 0:
            coinbase_sub_duration = coinbase_sub_30_days
        case 1:
            coinbase_sub_duration = coinbase_sub_90_days
        case 2:
            coinbase_sub_duration = coinbase_sub_365_days
    
    coinbase_checkout_info = {
        "name": f"Subscription for {coinbase_sub_duration} days",
        "description": user_telegram_id,
        "local_price": {
            "amount": coinbase_sub_duration,
            "currency": "USD"
        },
        "pricing_type": "fixed_price",
        "requested_info": ["email"]
    }

    coinbase_checkout_session = coinbase_client.checkout.create(**coinbase_checkout_info)

    return coinbase_base_url + coinbase_checkout_session["id"]