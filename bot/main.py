import os
from sqlalchemy import select
import sys
import telebot
from keyboa import Keyboa
import logging
from business import insert, select_all, db_session, Users, Topic, Message, init_migrate, select_max_id, delete

from help import extract_unique_code
from keyboard import start_keyboard_admin, start_keyboard_user, help_callback_keyboard

init_migrate()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
handler = logging.StreamHandler(sys.stdout)
telebot.logger.addHandler(handler)
telebot.logger.setLevel(logging.INFO)

teams = db_session.execute(select(Topic))
teams_count: int = sum(1 for _ in teams)


def get_user_id(username):
    res = select_all(Users, Users.username == username)
    return res[0].get("id") if res else None


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    unique_code = extract_unique_code(message.text) # получаем значение вместе с командой /start
    msg_json = message.json
    username = msg_json["from"].get("username")
    first_name = msg_json["from"].get("first_name")
    last_name = msg_json["from"].get("last_name")
    if get_user_id(username) is None:
        id_ = select_max_id(Users)
        id_ = id_ if id_ is not None else 0
        insert(Users, user_id=id_ + 1, first_name=first_name, last_name=last_name, username=username, admin=False,
               phone="")

    if unique_code:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Добро пожаловать, {username}! id из ссылки - {unique_code} "
                              f"Пожалуйста, выберите команду! <TODO: сделать входной текст>",
                         reply_markup=start_keyboard_admin())
        # ДОБАВИТЬ ПРОВЕРКУ НА ЮЗЕРА В БД И ПРИСВОЕНИЕ ID ТЕМЫ!!!

    else:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Добро пожаловать, {username}! Пожалуйста, выберите команду! <TODO: сделать входной текст>",
                         reply_markup=start_keyboard_user())


@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Тут будет помощь по боту", reply_markup=help_callback_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "create_topic")
def create_topic_callback(call):
    menu = [{'text': "Создать", 'callback_data': "push_topic"}, {'text': "Назад", 'callback_data': "back"}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Напишите название темы/команды/тэга: ", reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "topics_list")
def topics_list_callback(call):
    if teams_count == 0:
        menu = [{'text': "Назад", 'callback_data': "back"}]
        text = "Тэгов/команд пока что нет("
    else:
        menu = [{'text': x.name, 'callback_data': x.name} for x in teams] + [{'text': "Назад", 'callback_data': "back"}]
        text = "А вот и список команд:"
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text,
                          reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "creators")
def creators_callback(call):
    menu = [{'text': "Назад", 'callback_data': "back"}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Создатели: CyberFarshTeam", reply_markup=keyboard())


# Расположение клавиатуры для всех созданных команд
@bot.message_handler(commands=['teams', 'tags'])
def all_topics(message):
    if teams_count == 0:
        menu = ["Назад"]
        text = "Тэгов/команд пока что нет("
    else:
        menu = [x.name for x in teams] + ["Назад"]
        text = "А вот и список команд:"
    keyboard = Keyboa(items=menu)

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())


# Расположение клавиатуры для одной команды
@bot.message_handler(commands=['check_team'])
def exact_topic(message):
    menu = ["Просмотреть сообщения", "Получить список пользователей", "Создать рассылку", "Получить ссылку",
            "Удалить команду/тэг", "Назад"]
    keyboard = Keyboa(items=menu)
    text = "Вы выбрали тестовый тэг/команду для просмотра."
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())


# Начинается User-Side

# Расположение клавиатуры для одной команды
@bot.message_handler(commands=['send'])
def prepare_send_to_topic(message):
    teams = db_session.execute(select(Topic).join(Users).filter(Users.id == message.from_user.id))  # TODO Join-query
    teams_count: int = sum(1 for _ in teams)
    if teams_count == 0:
        menu = ["Выбрать команды/тэги", "Назад"]
        text = "У вас нет команд, в которых вы состоите! Выберите их:"
    else:
        menu = [x.name for x in teams] + ["Назад"]
        text = "Выберите тему/команду/тэг в которую хотите написать"
    keyboard = Keyboa(items=menu)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
