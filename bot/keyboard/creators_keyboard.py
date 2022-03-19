from keyboa import Keyboa


def creators_callback_keyboard(bot, call):
    menu = [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("$")[1]}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Создатели: CyberFarshTeam",
                          reply_markup=keyboard())