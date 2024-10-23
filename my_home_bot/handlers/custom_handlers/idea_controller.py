from loader import bot
from core.core import *
from keyboards import *


@bot.callback_query_handler(func=lambda call: call.data == "idea")
def handle_budget_button(call):
    """
    Обрабатывает нажатие кнопки "Предложить идею".

    :param call: объект CallbackQuery, содержащий информацию о нажатии кнопки
    """
    change_user(call.from_user.id, 'states', 'get_idea_budget')
    bot.delete_message(call.from_user.id, call.message.message_id)


    bot.send_message(call.from_user.id, 'Спасибо что используете мой бот, '
                                        'елси у вас есть идеи по улучшению '
                                        'или какие то дополнения, просто напишите их здесь:', reply_markup=start_menu_buttons())


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_idea_budget')
def get_new_idea(message):
    bot.send_message(message.from_user.id, 'Благодарю!', reply_markup=start_menu_buttons())
    bot.send_message(663078321, f"Пользователь с телеграм ID {message.from_user.id} оставил для вас пожелание: "
                                f"'{message.text}'\n"
                                f"Его данные: "
                                f"Имя: {message.from_user.first_name}\n"
                                f"Фамилия: {message.from_user.last_name if message.from_user.last_name else 'Не указана'}\n"
                                f"Юзернейм: @{message.from_user.username if message.from_user.username else 'Не указан'}\n"
                                f"ID чата: {message.chat.id}")


# Блокировка пользователя (бан)
def ban_user(chat_id, user_id):
    bot.kick_chat_member(chat_id, user_id)


# Разбан пользователя
def unban_user(chat_id, user_id):
    bot.unban_chat_member(chat_id, user_id)