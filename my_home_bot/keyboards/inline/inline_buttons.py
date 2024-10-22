from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta


def start_buttons():
    # кнопки в главном меню
    button1 = InlineKeyboardButton(text="Бюджет💰", callback_data="budget")
    button2 = InlineKeyboardButton(text="Задачки📒", callback_data="tasks")
    button3 = InlineKeyboardButton(text="Предложить идею💡", callback_data="idea")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    return keyboard


def start_budget_buttons(flag=False):
    # кнопки при нажатии на бюджет
    button1 = InlineKeyboardButton(text="Доход💴", callback_data="income")
    button2 = InlineKeyboardButton(text="Расход💸", callback_data="expend")
    button3 = InlineKeyboardButton(text="Копилка🏦", callback_data="piggy_bank")
    button4 = InlineKeyboardButton(text="Статистика📊", callback_data="statistic")
    button5 = InlineKeyboardButton(text="История правок🔧", callback_data="hist_budg")

    spacer = InlineKeyboardButton(text="\u2003", callback_data="none")

    # Создаем клавиатуру и добавляем кнопки
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1, button2)
    keyboard.add(button5)
    keyboard.add(spacer)
    keyboard.add(button3, button4)
    return keyboard


def start_menu_buttons(flag=False):
    # кнопка главное меню
    button1 = InlineKeyboardButton(text="Главное меню🏠", callback_data="main_menu")

    if flag:
        return button1
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1)
    return keyboard


def add_cat_buttons(cat_name:str, flag=False):
    # кнопка добавления категории
    button1 = InlineKeyboardButton(text="Добавить категорию", callback_data=cat_name)

    if flag:
        return button1
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1)
    return keyboard


def back_buttons(way:str, flag=False):
    # кнопка назад
    button1 = InlineKeyboardButton(text="Назад⏪", callback_data=way)

    if flag:
        return button1
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1)
    return keyboard


def create_or_connect_to_budgbase(flag=False):
    # кнопки создать и подключиться к базе бюджета
    button1 = InlineKeyboardButton(text="Создать", callback_data="create_base_budg")
    button2 = InlineKeyboardButton(text="Подключиться", callback_data="connect_base_budg")
    if flag:
        return button1, button2
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1, button2)
    return keyboard


def correct_task_buttons(text ,task_id, flag=False, delete_message=True):
    # изменить задачу
    delete_flag = '1' if delete_message else '0'
    button1 = InlineKeyboardButton(text, callback_data=f"correct_task_{task_id}_{delete_flag}")
    if flag:
        return button1
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1)
    return keyboard


def create_task(flag=False):
    # кнопка создания задачи
    button1 = InlineKeyboardButton('Добавить', callback_data=f"add_task")
    if flag:
        return button1
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1)
    return keyboard


def deposit_and_subtract(flag=False):
    button1 = InlineKeyboardButton('Добавить', callback_data=f"deposit")
    button2 = InlineKeyboardButton('Убавить', callback_data=f"subtract")
    if flag:
        return button1, button2
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1, button2)
    return keyboard


def task_edit_buttons(task_id, flag=False):
    """
        Создаёт кнопки для редактирования и удаления задачи.

        Аргументы:
        ----------
        task_id : int
            ID задачи, который будет передаваться в callback_data.

        Возвращает:
        -----------
        InlineKeyboardButton:
            Кнопки для редактирования и удаления.
        """
    button1 = InlineKeyboardButton('Удалить', callback_data=f"del_task_{task_id}")
    button2 = InlineKeyboardButton('Изменить', callback_data=f"edit_task_{task_id}")
    if flag:
        return button1, button2
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1, button2)
    return keyboard


def del_edit_money_buttons(money_id, flag=False):
    """
        Создаёт кнопки для редактирования и удаления записи в money_move.

        Аргументы:
        ----------
        money_id : int
            ID записи, который будет передаваться в callback_data.

        Возвращает:
        -----------
        InlineKeyboardButton:
            Кнопки для редактирования и удаления.
        """
    button1 = InlineKeyboardButton('Удалить', callback_data=f"del_mon_{money_id}")
    button2 = InlineKeyboardButton('Изменить', callback_data=f"ed_mon_{money_id}")
    if flag:
        return button1, button2
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1, button2)
    return keyboard


def create_history_buttons(history_data, current_page, total_pages):
    """
    Создает клавиатуру с кнопками на основе истории денежных перемещений
    и добавляет кнопки для навигации между страницами.
    """
    keyboard = InlineKeyboardMarkup()
    for record in history_data:
        category = record['category']
        income = record['income']
        expenditure = record['expenditure']
        comment = record['comment'] if record['comment'] else "Без комментария"
        record_id = record['id']

        # Определяем, что использовать в тексте: доход или расход
        if income != 0:
            text = f"{category}: 🤑{income} - '{comment}'"
        else:
            text = f"{category}: 🔻{expenditure} - '{comment}'"

        # Создаем кнопку с текстом
        button = InlineKeyboardButton(text=text, callback_data=f"edit_{record_id}")
        keyboard.add(button)

    # Добавляем кнопку "Загрузить еще", если есть следующая страница
    if current_page < total_pages-1:
        keyboard.add(InlineKeyboardButton(text="Загрузить еще", callback_data=f"load_more_{current_page + 1}"), back_buttons('budget', True))

    # Добавляем кнопку "Предыдущие", если не на первой странице
    if current_page > 0:
        keyboard.add(InlineKeyboardButton(text="Предыдущие", callback_data=f"load_previous_{current_page - 1}"), back_buttons('budget', True))

    if (current_page >= total_pages-1) and  (current_page <= 0):
        keyboard.add(back_buttons('budget', True))

    return keyboard



