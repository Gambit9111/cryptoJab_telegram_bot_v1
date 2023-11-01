import telebot

# init env variables and keys
import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")

# init telegram bot
telegram_bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY, parse_mode="HTML", num_threads=5)

@telegram_bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_bot.reply_to(message, "Howdy, how are you doing?")
    print(message)

def run():
    telegram_bot.polling()

run()