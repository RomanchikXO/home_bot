from loader import bot
from core.core import *
from keyboards import start_buttons




@bot.message_handler(commands=["start"])
def bot_start(message):
    user = check_or_add_user(message.from_user.id)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!",
                     reply_markup=start_buttons())

