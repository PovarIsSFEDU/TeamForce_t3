import logging
import os
import sys
import telebot
from sqlalchemy import and_
from keyboa import Keyboa
from business import insert, select_all, db_session, Users, Topic, Message, init_migrate, select_max_id, delete
from business import convert_to_list, get_theme_by_user, users_topic

from help import extract_unique_code
from keyboard import create_topic_keyboard, topics_list_keyboard, start_keyboard, help_callback_keyboard
from keyboard import creators_callback_keyboard, goback_callback_keyboard, exact_topic_keyboard
from keyboard import prepare_send_to_topic_keyboard
from keyboard import test_callback_keyboard, other_callback_keyboard, create_message_keyboard

from StateMachine import StateMachine, State
from TopicMachine import TopicMachine

init_migrate()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN

URL = f"https://t.me/{bot.get_me().username}"

handler = logging.StreamHandler(sys.stdout)
telebot.logger.addHandler(handler)
telebot.logger.setLevel(logging.DEBUG)

# teams = select_all(Topic)
# teams_count: int = sum(1 for _ in teams)

States = StateMachine()
Topics = TopicMachine()


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        if isinstance(message, telebot.types.CallbackQuery):
            return message.__dict__["from_user"].__dict__["id"] in get_admin_list()
        msg_dict = bot.get_chat_member(message.chat.id, message.from_user.id).__dict__
        user = msg_dict["user"].__dict__["id"] if msg_dict["user"] else False
        return user in get_admin_list()


def get_user_id(telegram_id):
    res = select_all(Users, Users.telegram_id == telegram_id)
    return res[0].get("users_id") if res else None


@convert_to_list
def get_admin_list():
    res = select_all(Users.telegram_id, Users.admin)
    return res


def check_auth(telegram_id):
    res = select_all(Users, Users.telegram_id == telegram_id)
    return res[0].get("users_admin") if res else False


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    teams = select_all(Topic)
    msg_json = message.json
    username, first_name = msg_json["from"].get("username"), msg_json["from"].get("first_name")
    telegram_id = msg_json["from"].get("id")
    AUTH_ADMIN = check_auth(telegram_id)
    last_name = msg_json["from"].get("last_name")
    id_theme = extract_unique_code(message.text)
    name_theme = None
    if id_theme:
        name_theme = select_all(Topic.name, operator=Topic.id == id_theme)[0]
        Topics.AddUser(message.chat.id)
        Topics.SetState(message.chat.id, id_theme)
    id_ = select_max_id(Users)
    if get_user_id(telegram_id) is None:
        insert(Users, user_id=id_ + 1, telegram_id=telegram_id, first_name=first_name, last_name=last_name, username=username, admin=AUTH_ADMIN,
               phone="")
    statement1 = users_topic.select().where(and_(users_topic.columns.topic_id == id_theme, users_topic.columns.users_id == get_user_id(telegram_id)))
    check_user_topic = db_session.execute(statement1).fetchall()

    if get_user_id(telegram_id) is not None and id_theme is not None and select_all(Topic.id, operator=Topic.id == id_theme) and not check_user_topic:
        statement = users_topic.insert().values(users_id=id_ + 1, topic_id=id_theme)
        db_session.execute(statement)
        db_session.commit()

    States.AddUser(message.chat.id)

    States.SetState(message.chat.id, State.Start)
    start_keyboard(bot, message, AUTH_ADMIN, id_theme, name_theme)


@bot.callback_query_handler(is_admin=True, func=lambda call: call.data.startswith("test"))
def edit_topic(call):
    pass


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=create_topic"))
def create_topic_callback(call):
    States.SetState(call.message.chat.id, State.CreateTopic)
    create_topic_keyboard(bot, call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=create_message"))
def create_message_callback(call):
    Topics.GetState(call.message.chat.id)
    test = get_theme_by_user(call.from_user.id)
    print(test)
    # create_message_keyboard(bot, call, name_theme)


@bot.message_handler(func=lambda msg: True)
def other1(call):
    msg_json = call.json
    name = msg_json.get("text")
    telegram_id = msg_json["from"].get("id")
    user_id = get_user_id(telegram_id)
    AUTH_ADMIN = check_auth(telegram_id)
    id_ = select_max_id(Topic)
    id_ = id_ if id_ is not None else 0
    try:
        if States.GetState(call.chat.id) == State.CreateTopic:
            insert(Topic, theme_id=id_+1, name=name, url=f"{URL}?start={id_+1}")
            statement = users_topic.insert().values(users_id=user_id, topic_id=id_+1)
            db_session.execute(statement)
            db_session.commit()

            bot.send_message(call.chat.id, f"Вы создали тему <b>{call.text}</b>.", parse_mode='HTML')

            start_keyboard(bot, call, AUTH_ADMIN, id_theme=None)
            States.SetState(call.chat.id, State.Start)
        else:
            bot.send_message(call.chat.id, "State not correct")
    except Exception as e:
        bot.reply_to(chat_id=call.chat.id,
                     message_id=call.message_id,
                     text='oooooooppppppssssss')


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=topics_list"))
def topics_list_callback(call):
    teams = select_all(Topic)
    topics_list_keyboard(bot, call, teams)


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
    bot.register_next_step_handler(call, other1)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&goback="))
def goback_callback(call):
    parent = call.data.split("&")[-1].split("=")[-1]
    tail = call.data.split("&")[1:-1]
    str_tail = ""
    for x in tail:
        str_tail += "&" + x
    call.data = str_tail
    goback_callback_keyboard(bot, call, parent, check_auth(call.__dict__["from_user"].__dict__["id"]), id_theme=None)


@bot.callback_query_handler(func=lambda call: call.data.startswith("&gotopic="))
def gotopic_callback(call):
    parent = call.data.split("&")[-1].split("=")[-1]
    tail = call.data.split("&")[1:-1]
    str_tail = ""
    for x in tail:
        str_tail += "&" + x
    call.data = str_tail
    goback_callback_keyboard(bot, call, parent, check_auth(call.__dict__["from_user"].__dict__["id"]), id_theme=None)


# Расположение клавиатуры для одной команды
@bot.message_handler(is_admin=True, commands=['check_team'])
def exact_topic(message):
    exact_topic_keyboard(bot, message)


# Начинается User-Side

# Расположение клавиатуры для одной команды
@bot.message_handler(commands=['send'])
def prepare_send_to_topic(message):
    id_ = get_user_id(message.from_user.id)
    teams = get_theme_by_user(id_)
    teams_count: int = len(teams)
    prepare_send_to_topic_keyboard(bot, message, teams, teams_count)


# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


bot.add_custom_filter(IsAdmin())

bot.infinity_polling()
