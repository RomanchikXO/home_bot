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
        bot.send_message(call.from_user.id, "Выберите категорию:", reply_markup=keyboard)
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
        bot.send_message(call.from_user.id, "Выберите категорию:", reply_markup=keyboard)
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
    user = check_or_add_user(message.from_user.id)
    global base
    if user.get('states') == 'get_sum_inc':
        money_move_change(float(message.text), 'income', base, user.get('id'), user.get('budget_id'))
        bot.send_message(message.from_user.id, 'Успешно', reply_markup=back_buttons('income'))
    elif user.get('states') == 'get_sum_exp':
        money_move_change(float(message.text), 'expenditure', base, user.get('id'), user.get('budget_id'))
        bot.send_message(message.from_user.id, 'Успешно', reply_markup=back_buttons('expend'))
    base = ''
    change_user(message.from_user.id, 'states', None)







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
            income_table.add_row([category, income])

    # Отправляем таблицу доходов, если она не пустая
    if income_table.rowcount > 0:
        bot.send_message(call.from_user.id, f"<pre>{income_table}</pre>", parse_mode='HTML')
    else:
        bot.send_message(call.from_user.id, "Нет данных по доходам.", parse_mode='HTML')

    # Создаем таблицу для расходов
    expenditure_table = PrettyTable()
    expenditure_table.field_names = ["Категория", "Расходы"]

    # Добавляем категории с ненулевыми расходами
    for category, expenditure in category_expenditure_totals.items():
        if expenditure > 0:  # Только категории с расходами больше 0
            expenditure_table.add_row([category, expenditure])

    # Отправляем таблицу расходов, если она не пустая
    if expenditure_table.rowcount > 0:
        bot.send_message(call.from_user.id, f"<pre>{expenditure_table}</pre>", parse_mode='HTML')
    else:
        bot.send_message(call.from_user.id, "Нет данных по расходам.", parse_mode='HTML')

    # Общая статистика
    overall_diff = total_income - total_expenditure

    # Формируем сообщение с общей статистикой
    stats_message = (
        f"<b>Общая статистика:</b>\n"
        f"Общие доходы: {total_income}\n"
        f"Общие расходы: {total_expenditure}\n"
        f"Разница: {overall_diff}"
    )

    # Отправляем общую статистику
    bot.send_message(call.from_user.id, stats_message, parse_mode='HTML', reply_markup=back_buttons('budget'))


