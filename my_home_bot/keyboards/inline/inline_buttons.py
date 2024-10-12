from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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

    # Создаем клавиатуру и добавляем кнопки
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button1, button2)
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






