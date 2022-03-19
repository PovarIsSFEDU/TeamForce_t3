from .start_keyboard import check_rules
from .creators_keyboard import creators_keyboard


def goback_callback_keyboard(bot, call, parent, AUTH_ADMIN):
    if parent == "start":
        text = "Добро пожаловать! Пожалуйста, выберите команду! <TODO: сделать входной текст>"
        reply_markup = check_rules(AUTH_ADMIN)
    elif parent == "creators":
        text = "Создатели: CyberFarshTeam"
        reply_markup = creators_keyboard(call)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text,
                          reply_markup=reply_markup)
