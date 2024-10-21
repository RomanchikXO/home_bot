from loader import bot
from core.core import *
from keyboards import *
from handlers.default_handlers.start import bot_start
from prettytable import PrettyTable



base = ''


@bot.callback_query_handler(func=lambda call: call.data == "budget")
def handle_budget_button(call):
    """
    Обрабатывает нажатие кнопки "Бюджет".

    :param call: объект CallbackQuery, содержащий информацию о нажатии кнопки
    """
    change_user(call.from_user.id, 'states', None)

    bot.delete_message(call.from_user.id, call.message.message_id)
    buttons = start_budget_buttons()
    keyboard = InlineKeyboardMarkup()
    user = check_or_add_user(call.from_user.id)
    if isinstance(user.get('budget_id'), int):
        base_budg = get_budget_by_id(user.get('budget_id'))

        buttons = start_budget_buttons()
        button1 = start_menu_buttons(True)
        tuple_buttons = create_or_connect_to_budgbase(True)
        button2 = tuple_buttons[0]
        button3 = tuple_buttons[1]
        buttons.add(button1)
        buttons.add(button2, button3)
        bot.send_message(call.from_user.id, f"База, {base_budg[0].get('name')} !",
                         reply_markup=buttons)

    else:
        button1 = start_menu_buttons(True)
        tuple_buttons = create_or_connect_to_budgbase(True)
        button2 = tuple_buttons[0]
        button3 = tuple_buttons[1]
        keyboard.add(button1)
        keyboard.add(button2, button3)
        bot.send_message(call.from_user.id, f"Привет, {call.from_user.first_name}!",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "income")
def push_income(call):
    # нажали доход
    bot.delete_message(call.from_user.id, call.message.message_id)
    user = check_or_add_user(call.from_user.id)

    keyboard = InlineKeyboardMarkup()
    add_cat = add_cat_buttons( 'income_cat_add', True)
    button_start = start_menu_buttons(True)
    back_button = back_buttons('budget', True)

    cats = get_categories(user.get('budget_id'), 'income')
    if len(cats) > 0:
        for cat in cats:
            button = InlineKeyboardButton(cat['category'], callback_data=f"categoryincome_{cat['category']}")
            keyboard.add(button)
        keyboard.add(add_cat, button_start)
        keyboard.add(back_button)
        bot.send_message(call.from_user.id, "Выберите категорию дохода:", reply_markup=keyboard)
    else:
        keyboard.add(add_cat, button_start)
        keyboard.add(back_button)
        bot.send_message(call.from_user.id, "Нет доступных категорий.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "income_cat_add")
def push_income_cat_add(call):
    # запрос новой категории для дохода
    bot.delete_message(call.from_user.id, call.message.message_id)
    change_user(call.from_user.id, 'states',  'get_inc_cat_from_user')
    bot.send_message(call.from_user.id, "ДОХОД: введи новую категорию", reply_markup=back_buttons('budget'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_inc_cat_from_user')
def get_cat_from_user(message):
    # сообщаем об успешном добавлении новой категории дохода
    change_user(message.from_user.id, 'states', None)
    user = check_or_add_user(message.from_user.id)
    res = get_categories(user.get('budget_id'), 'income')
    flag = True
    for r in res:
        if message.text == r.get('category'):
            flag = False
            break
    if not flag:
        bot.send_message(message.from_user.id, 'Такая категория уже существует, повтори поппытку: ',
                         reply_markup=back_buttons('budget'))
    else:
        create_cat(message.text, 'income', user.get('budget_id'))
        bot.send_message(message.from_user.id, f"Новая категория '{message.text}' успешно добавлена",
                         reply_markup=back_buttons('income'))


@bot.callback_query_handler(func=lambda call: call.data == "expend")
def push_expend(call):
    # нажали расход
    bot.delete_message(call.from_user.id, call.message.message_id)
    user = check_or_add_user(call.from_user.id)

    keyboard = InlineKeyboardMarkup()
    add_cat = add_cat_buttons( 'expend_cat_add', True)
    button_start = start_menu_buttons(True)
    back_button = back_buttons('budget', True)

    cats = get_categories(user.get('budget_id'), 'expense')
    if len(cats) > 0:
        for cat in cats:
            button = InlineKeyboardButton(cat['category'], callback_data=f"categoryexpend_{cat['category']}")
            keyboard.add(button)
        keyboard.add(add_cat, button_start)
        keyboard.add(back_button)
        bot.send_message(call.from_user.id, "Выберите категорию расхода:", reply_markup=keyboard)
    else:
        keyboard.add(add_cat, button_start)
        keyboard.add(back_button)
        bot.send_message(call.from_user.id, "Нет доступных категорий.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "expend_cat_add")
def push_income_cat_add(call):
    # запрос новой категории для расхода
    bot.delete_message(call.from_user.id, call.message.message_id)
    change_user(call.from_user.id, 'states',  'get_exp_cat_from_user')
    bot.send_message(call.from_user.id, "РАСХОД: введи новую категорию", reply_markup=back_buttons('budget'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_exp_cat_from_user')
def get_cat_from_user(message):
    # сообщаем об успешном добавлении новой категории расхода
    change_user(message.from_user.id, 'states', None)
    user = check_or_add_user(message.from_user.id)
    res = get_categories(user.get('budget_id'), 'expense')
    flag = True
    for r in res:
        if message.text == r.get('category'):
            flag = False
            break
    if not flag:
        bot.send_message(message.from_user.id, 'Такая категория уже существует, повтори поппытку: ',
                         reply_markup=back_buttons('budget'))
    else:
        create_cat(message.text, 'expense', user.get('budget_id'))
        bot.send_message(message.from_user.id, f"Новая категория '{message.text}' успешно добавлена",
                         reply_markup=back_buttons('expend'))







@bot.callback_query_handler(func=lambda call: call.data.startswith("categoryincome_"))
def handle_category_selection(call):
    # Нажали категорию дохода
    bot.delete_message(call.from_user.id, call.message.message_id)
    category_name = call.data.split('_', 1)[1]
    global base
    base = category_name

    change_user(call.from_user.id, 'states', 'get_sum_inc')
    bot.send_message(call.from_user.id, f"Введите сумму дохода: '{category_name}'", reply_markup=back_buttons('income'))
    # Здесь можно добавить дополнительные действия, например, обработать выбор категории


@bot.callback_query_handler(func=lambda call: call.data.startswith("categoryexpend_"))
def handle_category_selection(call):
    # Нажали категорию расхода
    bot.delete_message(call.from_user.id, call.message.message_id)
    category_name = call.data.split('_', 1)[1]
    global base
    base = category_name

    change_user(call.from_user.id, 'states', 'get_sum_exp')
    bot.send_message(call.from_user.id, f"Введите сумму расхода: '{category_name}'", reply_markup=back_buttons('expend'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') in ['get_sum_inc', 'get_sum_exp'])
def add_sum_to_money_move(message):
    # получаем сумму расхода/дохода, обрабатываем ее и заправшиваем коммент
    bot.delete_message(message.from_user.id, message.message_id)

    try:
        bot.delete_message(message.from_user.id, message.message_id - 1)
    except Exception as e:
        # Игнорируем ошибки, чтобы код продолжал выполнение
        pass
    user = check_or_add_user(message.from_user.id)
    print(user.get('states'))
    global base

    message_new = message.text.strip()
    try:
        message_new = float(message.text)
        base = {'name_cat': base, 'sum_money': message_new}

        if user.get('states') == 'get_sum_inc':
            bot.send_message(message.from_user.id, f"Введите комментарий для дохода в категории '{base['name_cat']}'",
                             reply_markup=back_buttons('income'))
            change_user(message.from_user.id, 'states', 'get_comm_inc')

        elif user.get('states') == 'get_sum_exp':
            bot.send_message(message.from_user.id, f"Введите комментарий для расхода в категории '{base['name_cat']}'",
                             reply_markup=back_buttons('expend'))
            change_user(message.from_user.id, 'states', 'get_comm_exp')

    except ValueError:
        bot.send_message(message.from_user.id, 'Некорректный ввод. Пожалуйста, введите число еще раз.', reply_markup=back_buttons('budget'))
        return



@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') in ['get_comm_inc', 'get_comm_exp'])
def add_comm_to_money_move(message):
    # получаем комментарий добавляем в базу money_move запись
    bot.delete_message(message.from_user.id, message.message_id)
    try:
        bot.delete_message(message.from_user.id, message.message_id - 1)
    except Exception as e:
        # Игнорируем ошибки, чтобы код продолжал выполнение
        pass

    user = check_or_add_user(message.from_user.id)
    global base


    if user.get('states') == 'get_comm_inc':
        money_move_change(base['sum_money'], 'income', base['name_cat'], user.get('id'), user.get('budget_id'), comm=message.text)
        bot.send_message(message.from_user.id, 'Успешно', reply_markup=back_buttons('income'))
    elif user.get('states') == 'get_comm_exp':
        money_move_change(base['sum_money'], 'expenditure', base['name_cat'], user.get('id'), user.get('budget_id'), comm=message.text)
        bot.send_message(message.from_user.id, 'Успешно', reply_markup=back_buttons('expend'))

    base = ''
    change_user(message.from_user.id, 'states', None)


@bot.callback_query_handler(func=lambda call: call.data == "hist_budg")
def handle_hist_budg(call):
    """
    Обрабатывает нажатие кнопки "История правок".
    Загружает первую страницу данных.
    """
    bot.delete_message(call.from_user.id, call.message.message_id)

    user_id = call.from_user.id  # Извлекаем ID пользователя Telegram
    user = check_or_add_user(user_id)  # Получаем данные пользователя из БД

    # Получаем последние 10 записей для этого пользователя
    history_data = get_history_for_user(user.get('id'), offset=0, limit=10)
    total_records = count_records(user.get('id'))  # Функция, чтобы узнать общее количество записей
    total_pages = (total_records // 10) + (1 if total_records % 10 else 0)

    keyboard = create_history_buttons(history_data, 0, total_pages)

    if not history_data:
        bot.send_message(call.from_user.id, "Нет данных для отображения.")
        return

    # Отправляем клавиатуру с историей
    bot.send_message(call.from_user.id, "История последних правок:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_"))
def handle_edit_record(call):
    """
    Обрабатывает нажатие кнопки редактирования записи.
    """
    user = check_or_add_user(call.from_user.id)
    record_id = int(call.data.split("_")[1])  # Получаем ID записи из callback_data
    bot.delete_message(call.from_user.id, call.message.message_id)

    record = money_move_select(user.get('budget_id'), record_id)[0]

    amount_type = "Доход" if record['income'] != 0 else "Расход"
    amount_value = record['income'] if record['income'] != 0 else record['expenditure']
    comment = record['comment'] if record['comment'] is not None else 'Без комментария'

    # Создание таблицы
    table = PrettyTable()

    # Добавляем по одной строке на каждое поле
    table.field_names = ["Параметр", "Значение"]
    table.add_row(["Категория", record['category']])
    table.add_row([amount_type, amount_value])
    table.add_row(["Комментарий", comment])
    table.max_width = 15  # Устанавливаем максимальную ширину
    table.align = "l"
    table_string = table.get_string()

    keyboard = InlineKeyboardMarkup()
    back_but = back_buttons('budget', True)
    del_but, edit_but = del_edit_money_buttons(record_id, True)

    keyboard.add(del_but, edit_but)
    keyboard.add((back_but))

    bot.send_message(
        call.from_user.id,
        f"Введите новые данные для записи ID {record_id}:\n\n```\n{table_string}\n```",
        reply_markup=keyboard,
        parse_mode='MarkdownV2'  # Используем MarkdownV2, чтобы текст форматировался правильно
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("del_mon_"))
def handle_del_money_record(call):
    # тут удаление записи в базе money_move
    bot.delete_message(call.from_user.id, call.message.message_id)
    user = check_or_add_user(call.from_user.id)

    rec_id = call.data.split('_')[2]  # Извлекаем ID записи из callback_data
    del_or_edit_task('del', rec_id)
    bot.send_message(call.from_user.id, 'Успешно удалено', reply_markup=back_buttons('hist_budg'))


@bot.callback_query_handler(func=lambda call: call.data.startswith("ed_mon_"))
def handle_edit_money_record(call):
    # тут запрос на изменение суммы в базе money_move
    bot.delete_message(call.from_user.id, call.message.message_id)
    rec_id = call.data.split('_')[2]


    bot.send_message(call.from_user.id, 'Пока в разработке', reply_markup=back_buttons('hist_budg'))

@bot.callback_query_handler(func=lambda call: call.data.startswith("load_more_"))
def handle_load_more(call):
    """
    Обрабатывает нажатие кнопки "Загрузить еще".
    """
    current_page = int(call.data.split("_")[2])  # Получаем текущую страницу
    user_id = call.from_user.id  # Извлекаем ID пользователя Telegram
    user = check_or_add_user(user_id)  # Получаем данные пользователя из БД

    # Получаем следующие 10 записей
    history_data = get_history_for_user(user.get('id'), offset=current_page * 10, limit=10)
    total_records = count_records(user.get('id'))  # Общее количество записей
    total_pages = (total_records // 10) + (1 if total_records % 10 else 0)

    keyboard = create_history_buttons(history_data, current_page, total_pages)

    if not history_data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.from_user.id, "Нет дополнительных данных для отображения.")
        return

    # Отправляем клавиатуру с историей
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("load_previous_"))
def handle_load_previous(call):
    """
    Обрабатывает нажатие кнопки "Предыдущие".
    """
    current_page = int(call.data.split("_")[2])  # Получаем текущую страницу
    user_id = call.from_user.id  # Извлекаем ID пользователя Telegram
    user = check_or_add_user(user_id)  # Получаем данные пользователя из БД

    # Получаем предыдущие 10 записей
    history_data = get_history_for_user(user.get('id'), offset=current_page * 10, limit=10)
    total_records = count_records(user.get('id'))  # Общее количество записей
    total_pages = (total_records // 10) + (1 if total_records % 10 else 0)

    keyboard = create_history_buttons(history_data, current_page, total_pages)

    if not history_data:
        bot.send_message(call.from_user.id, "Нет дополнительных данных для отображения.")
        return

    # Отправляем клавиатуру с историей
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == "create_base_budg")
def push_create_base_budg(call):
    # нажали кнопку создания базы бюджета
    bot.delete_message(call.from_user.id, call.message.message_id)
    change_user(call.from_user.id, 'states',  'get_name_new_base_budg')
    bot.send_message(call.from_user.id, 'Введи название базы', reply_markup=back_buttons('budget'))



@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_name_new_base_budg')
def get_name_new_base_budg(message):
    # создание базы: проверка введенного названия базы

    get_budg_bases = get_budget_by_id(name = message.text)
    if get_budg_bases:
        bot.send_message(message.from_user.id, "Название должно быть уникальным, повтори попытку: ")
    else:
        global base
        base = message.text
        change_user(message.from_user.id, 'states', 'get_pass_new_base_budg')
        bot.send_message(message.from_user.id, 'Введи пароль базы', reply_markup=back_buttons('budget'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_pass_new_base_budg')
def get_pass_new_base_budg(message):
    global base
    new_pass = encrypt_password(message.text)
    create_budgets(base, new_pass, message.from_user.id)
    base = ''
    bot.send_message(message.from_user.id, 'Вы успешно создали и подключились к новой базе, пожалуйста сохраните пароль', reply_markup=back_buttons('budget'))

@bot.callback_query_handler(func=lambda call: call.data == "connect_base_budg")
def push_connect_base_budg(call):
    # запрос имени базы ддя подключения
    bot.delete_message(call.from_user.id, call.message.message_id)
    change_user(call.from_user.id, 'states', 'get_name_base_budg')
    bot.send_message(call.from_user.id, 'Введи название базы', reply_markup=back_buttons('budget'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_name_base_budg')
def get_name_base_budg(message):
    # создание базы: проверка введенного названия базы

    get_budg_bases = get_budget_by_id(name = message.text)
    if get_budg_bases:
        global base
        base = get_budg_bases[0]
        change_user(message.from_user.id, 'states', 'get_pass_base_budg')
        bot.send_message(message.from_user.id, 'Введи пароль базы', reply_markup=back_buttons('budget'))
    else:
        bot.send_message(message.from_user.id, 'Кажется вы допустили ошибку, повторите попытку: ', reply_markup=back_buttons('budget'))


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') == 'get_pass_base_budg')
def get_pass_base_budg(message):
    global base

    check_pass = handle_password(message.text, base['pass'])

    if check_pass:
        base = ''
        bot.send_message(message.from_user.id, 'Вы подключились к новой базе', reply_markup=back_buttons('budget'))
    else:
        bot.send_message(message.from_user.id, 'Повтори попытку, пароль не верный', reply_markup=back_buttons('budget'))


@bot.callback_query_handler(func=lambda call: call.data == "statistic")
def handle_stat_button(call):
    """
    Обрабатывает нажатие кнопки "Статистика".
    """
    bot.delete_message(call.from_user.id, call.message.message_id)
    user = check_or_add_user(call.from_user.id)

    data = money_move_select(user.get('budget_id'))

    total_income = 0  # Общая сумма доходов
    total_expenditure = 0  # Общая сумма расходов
    category_income_totals = {}  # Словарь для хранения сумм доходов по категориям
    category_expenditure_totals = {}  # Словарь для хранения сумм расходов по категориям

    # Подсчет доходов и расходов
    for item in data:
        category = item['category']

        # Суммируем доходы
        total_income += item['income']
        if category not in category_income_totals:
            category_income_totals[category] = 0
        category_income_totals[category] += item['income']

        # Суммируем расходы
        total_expenditure += item['expenditure']
        if category not in category_expenditure_totals:
            category_expenditure_totals[category] = 0
        category_expenditure_totals[category] += item['expenditure']

    # Создаем таблицу для доходов
    income_table = PrettyTable()
    income_table.field_names = ["Категория", "Доходы"]

    # Добавляем категории с ненулевыми доходами
    for category, income in category_income_totals.items():
        if income > 0:  # Только категории с доходами больше 0
            income_table.add_row([category, int(income)])

    # Создаем таблицу для расходов
    expenditure_table = PrettyTable()
    expenditure_table.field_names = ["Категория", "Расходы"]

    # Добавляем категории с ненулевыми расходами
    for category, expenditure in category_expenditure_totals.items():
        if expenditure > 0:  # Только категории с расходами больше 0
            expenditure_table.add_row([category, int(expenditure)])

    # Общая статистика
    overall_diff = total_income - total_expenditure

    # Формируем сообщение с таблицами доходов, расходов и общей статистикой
    full_message = ""

    # Добавляем таблицу доходов, если она не пустая
    if income_table.rowcount > 0:
        full_message += f"<b>Доходы:</b>\n<pre>{income_table}</pre>\n"
    else:
        full_message += "Нет данных по доходам.\n"

    # Добавляем таблицу расходов, если она не пустая
    if expenditure_table.rowcount > 0:
        full_message += f"<b>Расходы:</b>\n<pre>{expenditure_table}</pre>\n"
    else:
        full_message += "Нет данных по расходам.\n"

    # Добавляем общую статистику
    full_message += (
        f"\n<b>Общая статистика:</b>\n"
        f"Общие доходы: {total_income}\n"
        f"Общие расходы: {total_expenditure}\n"
        f"Разница: {int(overall_diff)}"
    )

    # Отправляем всё как одно сообщение
    bot.send_message(call.from_user.id, full_message, parse_mode='HTML', reply_markup=back_buttons('budget'))



@bot.callback_query_handler(func=lambda call: call.data == "piggy_bank")
def handle_piggy_button(call):
    # нажали копилка
    bot.delete_message(call.from_user.id, call.message.message_id)
    keyboard = InlineKeyboardMarkup()
    main_menu = start_menu_buttons(True)
    dep_and_sub = deposit_and_subtract(True)
    keyboard.add(dep_and_sub[0], dep_and_sub[1])
    keyboard.add(main_menu)
    rec = 0

    user = check_or_add_user(call.from_user.id)
    records = get_piggy(user['budget_id'])
    if len(records) == 0:
        rec = 0
    else:
        rec = sum(record.get('money') if record.get('status') == 'dep' else -record.get('money') for record in records)

    bot.send_message(call.from_user.id, f'Сейчас в копилке: {rec} руб.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ["deposit", "subtract"])
def handle_piggy_button(call):
    # нажали добавить или убавить в копилке

    bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == "deposit":
        bot.send_message(call.from_user.id, 'Напишите сумму для добавления', reply_markup=back_buttons('budget'))
        change_user(call.from_user.id, 'states', 'add_dep')
    elif call.data == "subtract":
        bot.send_message(call.from_user.id, 'Напишите сумму для убавления', reply_markup=back_buttons('budget'))
        change_user(call.from_user.id, 'states', 'add_sub')


@bot.message_handler(func=lambda message: check_or_add_user(message.from_user.id).get('states') in ['add_dep', 'add_sub'])
def add_to_piggy(message):
    # добаление/убавление в копилку
    message_text = message.text.strip()
    try:
        amount = float(message_text)

        user = check_or_add_user(message.from_user.id)
        if user.get('states') == 'add_dep':
            edit_piggy(amount, user.get('budget_id'), 'dep')
            change_user(message.from_user.id, 'states', None)
            bot.send_message(message.from_user.id, 'Успешно!', reply_markup=back_buttons('budget'))
        elif user.get('states') == 'add_sub':
            edit_piggy(amount, user.get('budget_id'), 'sub')
            change_user(message.from_user.id, 'states', None)
            bot.send_message(message.from_user.id, 'Успешно!', reply_markup=back_buttons('budget'))
    except ValueError:
        bot.send_message(message.from_user.id, 'Некорректный ввод. Пожалуйста, введите число еще раз:', reply_markup=back_buttons('budget'))
        return


