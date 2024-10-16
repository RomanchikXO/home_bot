from loader import bot
from core.core import *
from keyboards import start_buttons




@bot.message_handler(commands=["start"])
def bot_start(message):
    user = check_or_add_user(message.from_user.id)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!",
                     reply_markup=start_buttons())



@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def handle_main_button(call):
    # нажали кнопку главное меню
    bot.delete_message(call.from_user.id, call.message.message_id)

    message = call.message
    message.from_user = call.from_user
    bot_start(message)