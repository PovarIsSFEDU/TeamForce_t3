import logging
import os
from sqlalchemy import select
import sys
import telebot
from keyboa import Keyboa
import logging
from business import insert, select_all, db_session, Users, Topic, Message, init_migrate, select_max_id, delete

from help import extract_unique_code
from keyboard import create_topic_keyboard, topics_list_keyboard, start_keyboard, help_callback_keyboard
from keyboard import creators_callback_keyboard, goback_callback_keyboard, exact_topic_keyboard
from keyboard import prepare_send_to_topic_keyboard
from keyboard import test_callback_keyboard, other_callback_keyboard

init_migrate()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
handler = logging.StreamHandler(sys.stdout)
telebot.logger.addHandler(handler)
telebot.logger.setLevel(logging.DEBUG)

teams = db_session.execute(select(Topic))
teams_count: int = sum(1 for _ in teams)
AUTH_ADMIN: bool = False


def get_user_id(username):
    res = select_all(Users, Users.username == username)
    return res[0].get("id") if res else None


def check_auth(username):
    res = select_all(Users, Users.username == username)
    return res[0].get("admin") if res else False


def auth(func):
    if AUTH_ADMIN:
        def foo(*args, **kwargs):
            func(*args, **kwargs)

        return foo()
    else:
        _ = lambda *args: None
        return _


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    msg_json = message.json
    username, first_name = msg_json["from"].get("username"), msg_json["from"].get("first_name")
    AUTH_ADMIN = check_auth(username)
    last_name = msg_json["from"].get("last_name")
    id_theme = extract_unique_code(message.text)
    if id_theme:
        # check_id_theme - это и будет id темы
        # Тут будет добавление темы для определенного пользователя, который перешёл по ссылке
        pass
    if get_user_id(username) is None:
        id_ = select_max_id(Users)
        id_ = id_ if id_ is not None else 0
        insert(Users, user_id=id_ + 1, first_name=first_name, last_name=last_name, username=username, admin=False,
               phone="")
    start_keyboard(bot, message, AUTH_ADMIN, id_theme)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=create_topic"))
def create_topic_callback(call):
    create_topic_keyboard(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=topics_list"))
def topics_list_callback(call):
    topics_list_keyboard(bot, call, teams_count, teams)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=help"))
def help_callback(call):
    help_callback_keyboard(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=creators"))
def creators_callback(call):
    creators_callback_keyboard(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=second"))
def creators_callback(call):
    test_callback_keyboard(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("push_topic"))
def edit_topics_callback(call):
    test_callback_keyboard(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=other_theme"))
def other_theme_callback(call):
    other_callback_keyboard(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&goback="))
def goback_callback(call):
    parent = call.data.split("&")[-1].split("=")[-1]
    tail = call.data.split("&")[1:-1]
    str_tail = ""
    for x in tail:
        str_tail += "&" + x
    call.data = str_tail
    goback_callback_keyboard(bot, call, parent, AUTH_ADMIN)


# Расположение клавиатуры для одной команды
@bot.message_handler(commands=['check_team'])
@auth
def exact_topic(message):
    exact_topic_keyboard(bot, message)


# Начинается User-Side

# Расположение клавиатуры для одной команды
@bot.message_handler(commands=['send'])
def prepare_send_to_topic(message):
    teams = db_session.execute(select(Topic).join(Users).filter(Users.id == message.from_user.id))  # TODO Join-query
    teams_count: int = sum(1 for _ in teams)
    prepare_send_to_topic_keyboard(bot, message, teams, teams_count)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()