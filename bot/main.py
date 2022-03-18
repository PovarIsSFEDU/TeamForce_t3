import logging
import os
from sqlalchemy import select
import sys
import telebot
from keyboa import Keyboa
import logging
from business import insert, select_all, db_session, User, Topic, Message, init_migrate

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
    menu = [{'text': "Создать тэг/команду", 'callback_data': "create_topic"}, {'text': "Список чатов", 'callback_data': "topics_list"}, {'text': "Помощь", 'callback_data': "help"}, {'text': "О создателях", 'callback_data': "creators"}]
    for point in menu:
        point["callback_data"] = "&target=" + point["callback_data"] + "$start"
    keyboard = Keyboa(items=menu)
    
    bot.send_message(chat_id=message.chat.id,
                     text="Добро пожаловать! Пожалуйста, выберите команду! <TODO: сделать входной текст>",
                     reply_markup=keyboard())





@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=create_topic"))
def create_topic_callback(call):
    menu = [{'text': "Создать", 'callback_data': "push_topic"}, {'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Напишите название темы/команды/тэга: ", reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=topics_list"))
def topics_list_callback(call):
    if (teams_count == 0):
        menu = [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
        text = "Тэгов/команд пока что нет("
    else:
        menu = [{'text': x.name, 'callback_data': x.name} for x in teams] + [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
        text = "А вот и список команд:"
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=help"))
def help_callback(call):
    menu = [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Тут будет помощь по боту", reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("&target=creators"))
def creators_callback(call):
    menu = [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Создатели: CyberFarshTeam", reply_markup=keyboard())




@bot.callback_query_handler(func=lambda call: call.data.startswith("&goback="))
def goback_callback(call):
    parent = call.data.split("=")[1]
    if parent == "start" :
        menu = [{'text': "Создать тэг/команду", 'callback_data': "create_topic"}, {'text': "Список чатов", 'callback_data': "topics_list"}, {'text': "Помощь", 'callback_data': "help"}, {'text': "О создателях", 'callback_data': "creators"}]
        for point in menu:
            point["callback_data"] = "&target=" + point["callback_data"] + "$start"
        text = "Добро пожаловать! Пожалуйста, выберите команду! <TODO: сделать входной текст>"
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard())




#Расположение клавиатуры для одной команды
@bot.message_handler(commands=['check_team'])
def exact_topic(message):
    menu = ["Просмотреть сообщения", "Получить список пользователей", "Создать рассылку", "Получить ссылку", "Удалить команду/тэг", "Назад"]
    keyboard = Keyboa(items=menu)
    text = "Вы выбрали тестовый тэг/команду для просмотра."
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard())




#Начинается User-Side

#Расположение клавиатуры для одной команды
@bot.message_handler(commands=['send'])
def prepare_send_to_topic(message):
    teams = db_session.execute(select(Topic).join(User).filter(User.id == message.from_user.id)) #TODO Join-query
    teams_count = sum(1 for _ in teams)
    text = ""
    if (teams_count == 0):
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
