import telebot
import os
import sys
import logging
from buiesnes import insert, select_all, db_session, Employ, Theme, Message, init_migrate

init_migrate()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
handler = logging.StreamHandler(sys.stdout)
telebot.logger.addHandler(handler)
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg_json = message.json
    username = msg_json["from"].get("username")
    first_name = msg_json["from"].get("first_name")
    last_name = msg_json["from"].get("last_name")
    insert(Employ, employ_id=1, first_name=first_name, last_name=last_name, username=username, admin=False, phone="")
    bot.reply_to(message, "Ботик жив и дразнит тебя")


@bot.message_handler(commands=['users'])
def get_users(message):
    res = select_all(Employ)
    bot.reply_to(message, "Ботик жив и дразнит тебя")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
