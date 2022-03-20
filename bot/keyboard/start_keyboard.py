from keyboa import Keyboa


def check_rules(auth, id_theme):
    if auth:  # клавиатура для админов
        return start_keyboard_admin()
    elif id_theme:  # клавиатура для людей, которые попали в бота по ссылке
        return start_keyboard_user_theme()
    else:  # клавиатура для людей, которые попали в бота НЕ по ссылке
        return start_keyboard_user()


def start_keyboard_admin():
    menu = [{'text': "Создать тэг/команду", 'callback_data': "create_topic"},
            {'text': "Список тем", 'callback_data': "topics_list"}, {'text': "Помощь", 'callback_data': "help"},
            {'text': "О создателях", 'callback_data': "creators"}]
    for point in menu:
        point["callback_data"] = "&target=" + point["callback_data"] + "$start"
    keyboard = Keyboa(items=menu)
    return keyboard()


def start_keyboard_user_theme():
    menu = [{'text': "Список моих тем", 'callback_data': "&my_list=all"}]
    keyboard = Keyboa(items=menu)
    return keyboard()


def start_keyboard_user():
    menu = [{'text': "Список тем", 'callback_data': "topics_list"}, {'text': "Помощь", 'callback_data': "help"},
            {'text': "О создателях", 'callback_data': "creators"}]
    for point in menu:
        point["callback_data"] = "&target=" + point["callback_data"] + "$start"
    keyboard = Keyboa(items=menu)
    return keyboard()


def start_keyboard(bot, message, AUTH_ADMIN, id_theme, name_theme):
    msg_json = message.json
    user_name = msg_json["from"].get("username")
    # get_name_theme = получение наименования темы по id из базы
    get_name_theme = "<b>Проект вселенского масштаба, в который нужны бэкендеры</b>"

    if id_theme:
        if AUTH_ADMIN:
            bot.send_message(chat_id=message.chat.id,
                             text="Добро пожаловать! Пожалуйста, выберите команду!",
                             reply_markup=check_rules(AUTH_ADMIN, id_theme=None), parse_mode="HTML")
        else:
            msg1 = "Пожалуйста пишите в чат."
            msg = f"Добро пожаловать {user_name}! Вы собираетесь ответить в тему: <b>{name_theme}</b>. {msg1}"
            bot.send_message(chat_id=message.chat.id,
                             text=msg, reply_markup=check_rules(AUTH_ADMIN, id_theme=id_theme),
                             parse_mode="HTML")
    else:
        if AUTH_ADMIN:
            bot.send_message(chat_id=message.chat.id,
                             text="Добро пожаловать! Пожалуйста, выберите команду!",
                             reply_markup=check_rules(AUTH_ADMIN, id_theme=None), parse_mode="HTML")
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="Добро пожаловать! У вас нет доступа к темам!",
                             reply_markup=check_rules(AUTH_ADMIN, id_theme=None))
