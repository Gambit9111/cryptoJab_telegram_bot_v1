from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

# data imports
from data import PRODUCTS
from data import PAYMENTS
from data import PREMIUM


# ! PRODUCTS KEYBOARD
products_factory = CallbackData('product_id', prefix='products')
class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


def products_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=product['emoji'] + '   ---   ' + product['name'] + '   |   ' + str(product['price']) + product['currency'] + '   ---   ' + product['emoji'],
                    callback_data=products_factory.new(product_id=product["id"])

                )
            ]
            for product in PRODUCTS
        ]
    )


# ! PREMIUM KEYBOARD
premium_factory = CallbackData('premium_id', prefix='premium')
class PremiumCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)
    
def premium_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=premium['emoji'] + '   ---   ' + premium['name'] + '   ---   ' + premium['emoji'],
                    callback_data=premium_factory.new(premium_id=premium["id"])

                )
            ]
            for premium in PREMIUM
        ]
    )

# ! CANCEL SUBSCRIPTION KEYBOARD

def cancel_subscription_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text='❌   ---   Cancel Subscription   ---   ❌',
                    callback_data='cancel_subscription'

                )
            ],
            [
                types.InlineKeyboardButton(
                    text='⬅        Go Back       ⬅',
                    callback_data='back_to_premium'
                )
            ]
        ]
    )


# ! PAYMENTS KEYBOARD
payments_factory = CallbackData('payment_id', prefix='payments')
class PaymentsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)

def payments_keyboard():
   
   payments_keyboard_list = [
       [
           types.InlineKeyboardButton(
               text=payment['emoji'] + '  ---  ' + payment['name'] + '  ---  ' + payment['emoji'],
               callback_data=payments_factory.new(payment_id=payment["id"])
           )
       ]
       for payment in PAYMENTS
   ]

   back_keyboard_list = [
       [
           types.InlineKeyboardButton(
               text='⬅        Go Back       ⬅',
               callback_data='back_to_products'
           )
       ]
   ]

   # Combine the two keyboards
   combined_keyboard_list = payments_keyboard_list + back_keyboard_list

   return types.InlineKeyboardMarkup(keyboard=combined_keyboard_list)
