import telebot
import os
import sys
import logging
from postgres import db_session, Employ, Theme, Message, init_migrate


init_migrate()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
handler = logging.StreamHandler(sys.stdout)
telebot.logger.addHandler(handler)
telebot.logger.setLevel(logging.INFO)


def insert_message(**kwargs):
    obj = Employ(**kwargs)
    db_session.add(obj)
    db_session.commit()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    name = message.json["from"].get("username")
    msg = message.json.get("date")
    insert_message(employ_id=1, name=name, project_name="АтласНКО", date_message=msg)
    bot.reply_to(message, "Ботик жив и дразнит тебя")


@bot.message_handler(commands=['users'])
def get_users(message):
    name = message.json["from"].get("username")
    msg = message.json.get("date")
    insert_message(employ_id=1, name=name, project_name="АтласНКО", date_message=msg)
    bot.reply_to(message, "Ботик жив и дразнит тебя")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
