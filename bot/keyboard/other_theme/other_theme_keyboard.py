from keyboa import Keyboa


def other_callback_keyboard(bot, call):
    # menu = [{'text': "Далее", 'callback_data': "&forward=" + call.data.split("$")[1]}]
    # keyboard = Keyboa(items=menu)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="Введите тему своего обращения, она будет отправлена администратору!")