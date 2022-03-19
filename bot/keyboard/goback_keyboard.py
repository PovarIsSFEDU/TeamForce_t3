from .start_keyboard import check_rules

def goback_callback_keyboard(bot, call, parent, AUTH_ADMIN):
    if parent == "start":
        text = "Добро пожаловать! Пожалуйста, выберите команду! <TODO: сделать входной текст>"
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text,
                          reply_markup=check_rules(AUTH_ADMIN))