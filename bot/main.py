import logging
import os
from sqlalchemy import select
import sys
import telebot
from keyboa import Keyboa
from postgres import db_session, User, Topic, Message, init_migrate
import logging
from buiesnes import insert, select_all, db_session, Employ, Theme, Message, init_migrate

init_migrate()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
handler = logging.StreamHandler(sys.stdout)
telebot.logger.addHandler(handler)
telebot.logger.setLevel(logging.INFO)

teams = db_session.execute(select(Topic))
teams_count = sum(1 for _ in teams)


@bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    menu = ["Создать тэг/команду", "Список чатов", "Помощь", "О создателях"]
    keyboard = Keyboa(items=menu)
    bot.send_message(chat_id=message.chat.id,
                     text="Добро пожаловать! Пожалуйста, выберите команду! <TODO: сделать входной текст>",
                     reply_markup=keyboard())


#Расположение клавиатуры для всех созданных команд
@bot.message_handler(commands=['teams', 'tags'])
def all_topics(message):
    if (teams_count == 0):
        menu = ["Назад"]
        text = "Тэгов/команд пока что нет("
    else:
        menu = [x.name for x in teams] + ["Назад"]
        text = "А вот и список команд:"
    keyboard = Keyboa(items=menu)

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())


#Расположение клавиатуры для одной команды
@bot.message_handler(commands=['check_team'])
def exact_topic(message):
    menu = ["Просмотреть сообщения", "Получить список пользователей", "Создать рассылку", "Получить ссылку", "Удалить команду/тэг", "Назад"]
    keyboard = Keyboa(items=menu)
    text = "Вы выбрали тестовый тэг/команду для просмотра."
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())


#@bot.message_handler(commands=['team', 'tag'])
#def topic_creation(message):
#
#   bot.reply_to(message, "Команда(тэг) создана. А вот и ссылка для присоединения: " + "start=")



#Начинается User-Side

#Расположение клавиатуры для одной команды
@bot.message_handler(commands=['send'])
def prepare_send_to_topic(message):
    teams = db_session.execute(select(Topic).join(User).filter(User.id == message.from_user.id)) #TODO Join-query
    teams_count = sum(1 for _ in teams)
    if (teams_count == 0):
        menu = ["Выбрать команды/тэги", "Назад"]
        text = "У вас нет команд, в которых вы состоите! Выберите их:"
    else:
        menu = [x.name for x in teams] + ["Назад"]
        text = "Выберите тему/команду/тэг в которую хотите написать"
    keyboard = Keyboa(items=menu)
    text = "После этого вы напишете тестовое сообщение."
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())




@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
