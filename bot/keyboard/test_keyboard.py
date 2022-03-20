from keyboa import Keyboa


def test_callback_keyboard(bot, call):
    #tail = call.data.split("&")[1:-1]
    #str_tail = ""
    #for x in tail:
        #str_tail += "&" + x
    menu = [{'text': "Назад", 'callback_data': "&goback=" + call.data.split("&")[-1].split("=")[-1]}]
    keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Второй уровень вложенности",
                          reply_markup=keyboard())