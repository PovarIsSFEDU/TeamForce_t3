from keyboa import Keyboa


def creators_keyboard(call):
    tail = call.data.split("&")[1:-1]
    str_tail = ""
    for x in tail:
        str_tail += "&" + x
    menu = [{'text': "⬅ Назад", 'callback_data': "&goback=start"},
            {'text': "Второй уровень", 'callback_data': "&target=second&creators"}]
    keyboard = Keyboa(items=menu)
    return keyboard()

def creators_callback_keyboard(bot, call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Наименование команды: CyberFarsh \n\nЧлены команды: \n1) Рындин Денис (@pustoiden)\n"
                               "2) Лукаш Павел (@p0varReal)\n"
                               "3) Юров Ярослав (@matlog)",
                          reply_markup=creators_keyboard(call))




