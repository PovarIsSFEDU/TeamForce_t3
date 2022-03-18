from keyboa import Keyboa


def help_callback_keyboard():
    menu = [{'text': "Назад", 'callback_data': "back"}]
    keyboard = Keyboa(items=menu)
    return keyboard()