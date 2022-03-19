from keyboa import Keyboa
from telebot import types

def create_topic_keyboard(bot, call):
    #menu = [{'text': "Создать", 'callback_data': "push_topic"},
    #        {'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
    #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #create_button = types.KeyboardButton('Создать')
    #back_button = types.KeyboardButton('Назад')
    #markup.row(create_button, back_button)
    bot.send_message(chat_id=call.message.chat.id,
                          text="Напишите название темы/команды/тэга: ")
                          #reply_markup=markup)


def topics_list_keyboard(bot, call, teams_count, teams):
    if teams_count == 0:
        menu = [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
        text = "Тэгов/команд пока что нет("
    else:
        menu = [{'text': x.get("topic_name"), 'callback_data': x.get("topic_name")} for x in teams] + [
            {'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
        text = "А вот и список команд:"
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text,
                          reply_markup=keyboard())