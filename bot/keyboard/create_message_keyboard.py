def create_message_keyboard(bot, call, name_theme):
    bot.send_message(chat_id=call.message.chat.id,
                     text=f"Напишите сообщение в тему: {name_theme}")