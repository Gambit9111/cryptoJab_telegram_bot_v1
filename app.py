from telebot import types, TeleBot
import datetime

# * IMPORTANT
# ! ATEENTION
# ? QUESTION
# TODO: TO DO
# // REMOVED

import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_API_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")
bot = TeleBot(TELEGRAM_BOT_API_TOKEN, num_threads=4, parse_mode="HTML")

# data imports
from data import PRODUCTS
from data import PAYMENTS
from data import WELCOME_MESSAGE

# db imports
from db import Database

# keyboard imports
from keyboard_handler import products_factory, products_keyboard, premium_keyboard, payments_factory, payments_keyboard, premium_factory, cancel_subscription_keyboard, ProductsCallbackFilter

# checkout imports
from coinbase_checkout_handler import create_coinbase_checkout_session
from stripe_checkout_handler import create_stripe_checkout_session


# ! TEST VARIABLES
premium_user = False
joined_group = False
valid_until_date_time = "2023-12-12 10:10"
admin_user = False


# user_data = {user_telegram_id: product_id}
user_data = {}
db = Database()


# ! START COMMAND ------------------------------>>
@bot.message_handler(commands=['start']) 
def start_command_handler(message: types.Message):

    # get the user id
    user_telegram_id = str(message.from_user.id)

    print("User: " + user_telegram_id + " started the bot")

    # * if user has already selected a product delete it
    if user_telegram_id in user_data:
        user_data.pop(user_telegram_id, None)
    
    bot.send_message(message.chat.id, WELCOME_MESSAGE)

    # * fetch user from db by telegram id to check if hes premium
    user = db.fetchone("SELECT * FROM users WHERE telegram_id = %s", (user_telegram_id,))

    # * if user exists in the database he is premium
    if user:
        premium_user = True
        valid_until_date_time = user[5]
        print("User: " + user_telegram_id + " is premium")

    # ? PREMIUM USER MENU
    if premium_user:
        # calculate duration left
        duration_left = datetime.datetime.strptime(valid_until_date_time, '%Y-%m-%d %H:%M') - datetime.datetime.now()
        # create a markup text to show premium duration
        text = f"Your premium subscription is valid until {valid_until_date_time}\n" \
               f"Duration left: {duration_left.days} days {duration_left.seconds // 3600} hours"
        
        # ! SEND USER THE PREMIUM MENU  ->>>
        # change keyboard to premium keyboard
        bot.send_message(user_telegram_id, text=text, reply_markup=premium_keyboard())
        return

    # ? NEW USER MENU                 # ! SEND USER THE PRODUCTS MENU  ->>>
    bot.send_message(user_telegram_id, "Please select your subscription plan 🚀:", reply_markup=products_keyboard())

    print(user_data)


# ! WILL FIRE AFTER ANY PRODUCT IS SELECTED
@bot.callback_query_handler(func=None, config=products_factory.filter())
def products_callback(call: types.CallbackQuery):

    # get the user id
    user_telegram_id = str(call.from_user.id)

    # check if user has already selected a product
    if user_telegram_id in user_data:
        # remove the product from user_data list
        user_data.pop(user_telegram_id, None)
    
    # get the product from callback
    callback_data: dict = products_factory.parse(callback_data=call.data)
    product_id = int(callback_data['product_id'])

    # get the product from data file
    product = PRODUCTS[product_id]
    # * product_id = 0 | 30 days | 45$
    # * product_id = 1 | 90 days | 120$
    # * product_id = 2 | 365 days | 365$

    # create a markup for the payment methods
    text = f"Subscription for CryptoJab 🚀🚀🚀: {product['name']}\n" \
           f"Price: {product['price']} {product['currency']}\n"

    # save the product id to the user_data list
    user_data[user_telegram_id] = product_id
    print("User: " + str(call.message.chat.id) + " selected product: " + str(product_id))

    # ! SEND USER THE PAYMENT METHODS MENU WITH A BACK BUTTON THAT WILL GO BACK TO THE PRODUCTS MENU
    # change keyboard to payment methods
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=payments_keyboard())
    
    print(user_data)

# ! <------------- GOES BACK TO THE PRODUCTS MENU
@bot.callback_query_handler(func=lambda c: c.data == 'back_to_products')
def back_to_products_callback(call: types.CallbackQuery):

    # get the user id
    user_telegram_id = str(call.from_user.id)

    # remove the product from user_data list
    user_data.pop(user_telegram_id, None)

    # ! SEND USER THE PRODUCTS MENU
    # change keyboard to products keyboard
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Please select your subscription plan 🚀:", reply_markup=products_keyboard())
    
    print("User: " + str(call.message.chat.id) + " went back to products")

    print(user_data)

# ! WILL FIRE AFTER ANY PAYMENT METHOD IS SELECTED
@bot.callback_query_handler(func=None, config=payments_factory.filter())
def payments_callback(call: types.CallbackQuery):

    # get the user id
    user_telegram_id = str(call.from_user.id)

    # check if user has already selected a product
    if user_telegram_id not in user_data:
        bot.answer_callback_query(callback_query_id=call.id, text='Please select a product first', show_alert=True)
        return
    
    # get the product from user_data list
    chosen_product_id = user_data[user_telegram_id]

    # get the product from data file
    product = PRODUCTS[chosen_product_id]
    # * product_id = 0 | 30 days | 45$
    # * product_id = 1 | 90 days | 120$
    # * product_id = 2 | 365 days | 365$

    # get the payment from callback
    callback_data: dict = payments_factory.parse(callback_data=call.data)
    payment_id = int(callback_data['payment_id'])

    # get the payment from data file
    payment = PAYMENTS[payment_id]
    # * payment_id = 0 | STRIPE
    # * payment_id = 1 | COINBASE

    # create a markup for the payment methods
    text = f"Subscription for CryptoJab 🚀🚀🚀: {product['name']}\n" \
           f"Price: {product['price']} {product['currency']}\n" \
           f"Payment method: {payment['name']}"

    print("User: " + str(call.message.chat.id) + " selected payment: " + str(payment_id))


    # // TODO send user the payment link

    match payment_id:
        case 0:  #? STRIPE
            
            # * create stripe checkout session
            stripe_checkout_session_url = create_stripe_checkout_session(user_telegram_id, chosen_product_id)

            # * create checkout message
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="Buy Subscription 🚀", url=stripe_checkout_session_url))

            # * send user the checkout message
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                        text=text, reply_markup=markup)
            return
        
        case 1: #? COINBASE
            
            # * create coinbase checkout session
            coinbase_checkout_session_url = create_coinbase_checkout_session(user_telegram_id, chosen_product_id)
            
            # * create checkout message
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="Buy Subscription 🚀", url=coinbase_checkout_session_url))

            # * send user the checkout message
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                        text=text, reply_markup=markup)
            return
        
    print(user_data)

# ! WILL FIRE AFTER ANY PREMIUM OPTION IS SELECTED IF USER IS PREMIUM
# ? IF USER IS PREMIUM
@bot.callback_query_handler(func=None, config=premium_factory.filter())
def premium_callback(call: types.CallbackQuery):

    # get the user id
    user_telegram_id = str(call.from_user.id)

    # get the product from callback
    callback_data: dict = premium_factory.parse(callback_data=call.data)
    premium_id = int(callback_data['premium_id'])

    # * premium_id = 0 | join the vip channel
    # * premium_id = 1 | cancel the subscription

    print(user_telegram_id, premium_id)

    match premium_id:
        case 0:  #? join the vip channel
        # TODO check if the user is in the group already, notify him if he is, otherwise send him the invite link
            if joined_group:
                bot.answer_callback_query(callback_query_id=call.id, text='You are already in the group', show_alert=True)
                return
            else:
                # ! send user invite link to the group
                text = "Join the group: https://t.me/joinchat/AAAAAFh6X1ZjZjYx"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text)
                return
        case 1:  #? cancel the subscription
            # Create a markup for subscription cancelation, warn the user that if he cancels the sub he will be kicked out of the group iommediately
            text = f"❌ Are you sure you want to cancel your subscription? If you cancel the subscription now, you will not be able to access the VIP group anymore! ❌"

            # change keyboard to cancel subscription keyboard
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=cancel_subscription_keyboard())
            return




# ! WILL FIRE AFTER SUBSCRIPTION CANCELATION IS CONFIRMED
@bot.callback_query_handler(func=lambda c: c.data == 'cancel_subscription' or c.data == 'back_to_premium')
def cancel_subscription_callback(call: types.CallbackQuery):

    # get the user id
    user_telegram_id = str(call.from_user.id)

    # check which callback was called
    if call.data == 'cancel_subscription':
        # TODO cancel the subscription
        print(user_telegram_id, "canceled the sub")
        text= "Your subscription has been canceled and you no longer have an access to the group"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text)
        return
    
    # send the user back to premium menu
    if call.data == 'back_to_premium':
        # calculate duration left
        duration_left = datetime.datetime.strptime(valid_until_date_time, '%Y-%m-%d %H:%M') - datetime.datetime.now()
        # create a markup text to show premium duration
        text = f"Your premium subscription is valid until {valid_until_date_time}\n" \
               f"Duration left: {duration_left.days} days {duration_left.seconds // 3600} hours"
        
        # ! SEND USER THE PREMIUM MENU  ->>>
        # change keyboard to premium keyboard
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=premium_keyboard())
        return

# ! Only product with field - product_id = 2 MAKE CHOICE UNAVAILABLE
# // @bot.callback_query_handler(func=None, config=products_factory.filter(product_id='2'))
# // def product_one_callback(call: types.CallbackQuery):
# //    bot.answer_callback_query(callback_query_id=call.id, text='Not available :(', show_alert=True)

bot.add_custom_filter(ProductsCallbackFilter())
bot.infinity_polling()