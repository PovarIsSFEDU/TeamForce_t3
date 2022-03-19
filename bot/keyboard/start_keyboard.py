from keyboa import Keyboa


def check_rules(auth):
    if auth:
        return start_keyboard_admin()
    else:
        return start_keyboard_user()


def start_keyboard_admin():
    menu = [{'text': "Создать тэг/команду", 'callback_data': "create_topic"},
            {'text': "Список тем", 'callback_data': "topics_list"}, {'text': "Помощь", 'callback_data': "help"},
            {'text': "О создателях", 'callback_data': "creators"}]
    for point in menu:
        point["callback_data"] = "&target=" + point["callback_data"] + "$start"
    keyboard = Keyboa(items=menu)
    return keyboard()


def start_keyboard_user():
    menu = [{'text': "Список тем", 'callback_data': "topics_list"}, {'text': "Помощь", 'callback_data': "help"},
            {'text': "О создателях", 'callback_data': "creators"}]
    for point in menu:
        point["callback_data"] = "&target=" + point["callback_data"] + "$start"
    keyboard = Keyboa(items=menu)
    return keyboard()


def start_keyboard(bot, message, AUTH_ADMIN, id_theme):
    if id_theme:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Добро пожаловать! Тема обращения ID - {id_theme}",
                         reply_markup=check_rules(AUTH_ADMIN))
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Добро пожаловать! Пожалуйста, выберите тему обращения!",
                         reply_markup=check_rules(AUTH_ADMIN))
