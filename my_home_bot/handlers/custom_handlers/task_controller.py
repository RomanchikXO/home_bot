from loader import bot
from core.core import *
from keyboards import *
from datetime import datetime

some_data = {}


@bot.callback_query_handler(func=lambda call: call.data == "tasks")
def handle_tasks_button(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    user = check_or_add_user(call.from_user.id)
    user_tasks = get_tasks(user.get('id'))

    keyboard = InlineKeyboardMarkup()  # Инициализация клавиатуры
    start_menu = start_menu_buttons(True)
    create = create_task(True)

    if user_tasks:
        task_messages = []  # Список для хранения сообщений о задачах
        for task in user_tasks:
            task_status = "🟢|" if task['status'] == 'new' else "🔴|"  # Зеленый круг для новых задач
            task_text = task['task']
            task_date = str(datetime.fromtimestamp(task['plane_date']).strftime('%d.%m'))+ "|"  # Форматирование даты


            message = task_status + task_date + task_text
            button = correct_task_buttons(message, task['id'], True)
            keyboard.add(button)



        keyboard.add(start_menu, create)

        bot.send_message(call.from_user.id,  'Задачи', reply_markup=keyboard)
    else:
        keyboard.add(start_menu, create)
        bot.send_message(call.from_user.id, 'Задачь пока что нет', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("correct_task_"))
def handle_edit_task(call):
    # тут будет редактирование задачи
    try:
        some, _, task_id, delete_flag = call.data.split('_')
        # Проверяем, нужно ли удалять сообщение
        if delete_flag == '1':
            bot.delete_message(call.from_user.id, call.message.message_id)
    except Exception as e:
        pass
    user = check_or_add_user(call.from_user.id)

    task_id = call.data.split('_')[2]  # Извлекаем ID задачи из callback_data
    task = get_tasks(id_user=user.get('id'), id_task=int(task_id))[0]
    message = f"Плановая дата: {convert_unix_time(task['plane_date'], 'дд.мм.гггг')}\n"
    message += f"Статус: {'Новая' if task['status'] == 'new' else 'Просрочена'}\n\n"
    message += f"Задача: {task['task']}\n"
    back_but = back_buttons('tasks', True)

    del_but, ed_but = task_edit_buttons(int(task_id), True)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(del_but, ed_but)
    keyboard.add(back_but)
    bot.send_message(call.from_user.id, message, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("del_task_"))
def handle_del_task(call):
    # удалить задачу
    bot.delete_message(call.from_user.id, call.message.message_id)
    task_id = call.data.split('_')[2]
    delete_task(task_id)
    bot.send_message(call.from_user.id, 'Задача удалена', reply_markup=back_buttons('tasks'))


@bot.callback_query_handler(func=lambda call: call.data.startswith("task_edit_"))
def handle_correct_task(call):
    #редактировать задачу
    bot.delete_message(call.from_user.id, call.message.message_id)
    task_id = call.data.split('_')[2]
    bot.send_message(call.from_user.id, 'Пока в разработке', reply_markup=back_buttons('tasks'))




@bot.callback_query_handler(func=lambda call: call.data == "add_task")
def handle_add_task(call):
    # добавить задачу
    bot.delete_message(call.from_user.id, call.message.message_id)
    change_user(call.from_user.id, 'states', 'add_task')
    bot.send_message(call.from_user.id, 'Напишите новую задачу', reply_markup=back_buttons('tasks'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'add_task')
def add_new_task(message):
    global some_data
    some_data = message.text

    show_calendar(message.from_user.id, datetime.utcnow() + timedelta(hours=3))




def show_calendar(user_id, date):
    # Получаем первый и последний день месяца
    first_day = date.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Создаем инлайн-клавиатуру для календаря
    keyboard = InlineKeyboardMarkup()

    # Заголовок с месяцем и годом
    header = f"{first_day.strftime('%B %Y')}"

    # Получаем текущую дату
    today = (datetime.utcnow() + timedelta(hours=3)).date()

    # Убираем кнопку "<" если календарь на текущем месяце
    if first_day.month == today.month and first_day.year == today.year:
        keyboard.row(
            InlineKeyboardButton(" ", callback_data="ignore"),
            InlineKeyboardButton(header, callback_data="ignore"),
            InlineKeyboardButton(">", callback_data=f"next_month_{first_day.month}_{first_day.year}")
        )
    else:
        keyboard.row(
            InlineKeyboardButton("<", callback_data=f"prev_month_{first_day.month}_{first_day.year}"),
            InlineKeyboardButton(header, callback_data="ignore"),
            InlineKeyboardButton(">", callback_data=f"next_month_{first_day.month}_{first_day.year}")
        )

    # День недели, с которого начинается месяц (понедельник = 0, воскресенье = 6)
    start_weekday = (first_day.weekday() + 6) % 7  # Переводим так, чтобы понедельник был началом
    if start_weekday != 0:
        start_weekday += 1

    # Добавляем пустые кнопки до первого дня месяца, если месяц не начинается с понедельника
    week = []
    for _ in range(start_weekday):
        week.append(InlineKeyboardButton(" ", callback_data="ignore"))

    # Добавляем дни месяца
    for day in range(1, (last_day - first_day).days + 2):
        current_date = first_day.replace(day=day).date()

        if current_date < today and current_date >= today - timedelta(days=today.weekday()):
            # Дни на текущей неделе, которые уже прошли, делаем пустыми
            week.append(InlineKeyboardButton(" ", callback_data="ignore"))
        elif current_date >= today:
            # Доступные для выбора дни
            week.append(InlineKeyboardButton(f"{day}", callback_data=f"select_date_{current_date.strftime('%d.%m.%Y')}"))

        # Добавляем неделю в клавиатуру, если она полная (7 кнопок)
        if len(week) == 7:
            keyboard.row(*week)
            week = []

    # Добавляем дни следующего месяца до завершения последней недели
    next_month_day = 1
    while len(week) < 7:
        current_date = last_day + timedelta(days=next_month_day)
        week.append(InlineKeyboardButton(f"{next_month_day}", callback_data=f"select_date_{current_date.strftime('%d.%m.%Y')}"))
        next_month_day += 1

    if week:
        keyboard.row(*week)

    # Кнопка для возврата
    keyboard.row(InlineKeyboardButton("Назад", callback_data='tasks'))

    bot.send_message(user_id, "Выберите дату:", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_month_"))
def handle_prev_month(call):
    bot.delete_message(call.from_user.id, call.message.message_id)

    # Разбиваем данные и извлекаем месяц и год
    try:
        month, year = map(int, call.data.split("_")[2:])  # Извлечение месяца и года
        # Уменьшаем месяц и проверяем на переполнение
        if month == 1:  # Январь
            month = 12
            year -= 1
        else:
            month -= 1
        date = datetime(year, month, 1)
        show_calendar(call.from_user.id, date)
    except ValueError:
        bot.send_message(call.from_user.id, "Произошла ошибка при выборе месяца. Попробуйте снова.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("next_month_"))
def handle_next_month(call):
    bot.delete_message(call.from_user.id, call.message.message_id)

    month, year = map(int, call.data.split("_")[2:])  # Извлечение месяца и года
    # Увеличиваем месяц и проверяем на переполнение
    if month == 12:  # Декабрь
        month = 1
        year += 1
    else:
        month += 1
    date = datetime(year, month, 1)
    show_calendar(call.from_user.id, date)



@bot.callback_query_handler(func=lambda call: call.data.startswith("select_date_"))
def handle_date_selection(call):
    user = check_or_add_user(call.from_user.id)
    global some_data
    bot.delete_message(call.from_user.id, call.message.message_id)
    selected_date = call.data.split("_")[2]  # Извлекаем выбранную дату
    unix_select_date = convert_to_unix(selected_date)

    add_task(user.get('id'), some_data, unix_select_date)

    bot.send_message(call.from_user.id, f"Задача '{some_data}' добавлена !", reply_markup=back_buttons('tasks'))


