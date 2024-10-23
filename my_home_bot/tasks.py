from datetime import datetime

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import start_menu_buttons, create_task, correct_task_buttons
from loader import bot
from core.core import get_unix_to_day
from database.DataBase import connect_to_database
import psycopg2.extras
from itertools import groupby
from operator import itemgetter


def get_celery_app():
    from celery_app import app  # Импортируем внутри функции, чтобы избежать цикла
    return app


@get_celery_app().task
def check_tasks():
    conn = connect_to_database()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            now = get_unix_to_day()

            # Выбираем задачи, которые нужно выполнить
            cursor.execute("""
                SELECT tk.*, ac.tg_id FROM task as tk JOIN accounts ac on tk.id_user=ac.id WHERE plane_date=%s ORDER BY tk.id_user ASC
            """, (now,))
            tasks = cursor.fetchall()

            if tasks:
                result = [
                    {
                        'tg_id': tg_id,
                        'tasks': [
                            {'id': row['id'], 'id_user': row['id_user'], 'task': row['task'], 'status': row['status'],
                             'plane_date': row['plane_date']}
                            for row in group
                        ]
                    }
                    for tg_id, group in groupby(tasks, key=itemgetter('tg_id'))
                ]

                start_menu = start_menu_buttons(True)
                create = create_task(True)

                for user_tasks in result:
                    tg_id = user_tasks['tg_id']
                    keyboard = InlineKeyboardMarkup()

                    message_text = "Задачи на сегодня:\n"

                    # Формируем сообщение из всех задач пользователя
                    for task in user_tasks['tasks']:
                        task_status = "🟢|" if task['status'] == 'new' else "🔴|"
                        task_text = task['task']
                        task_date = str(datetime.fromtimestamp(task['plane_date']).strftime('%d.%m')) + "|"

                        # Формируем текст для задачи
                        task_message = task_status + task_date + task_text

                        # Кнопка для каждой задачи
                        button = correct_task_buttons(task_message, task['id'], True, False)
                        keyboard.add(button)

                    keyboard.add(start_menu, create)
                    bot.send_message(tg_id, message_text, reply_markup=keyboard)

            else:
                print("Задач на выполнение нет.")

            conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()


@get_celery_app().task
def old_tasks():
    conn = connect_to_database()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            yesterday = get_unix_to_day() - 86400

            # Выбираем задачи, которые нужно выполнить
            cursor.execute("""
                SELECT id FROM task WHERE plane_date<=%s 
            """, (yesterday,))
            tasks = cursor.fetchall()
            if tasks:
                task_ids = [row['id'] for row in tasks]
                if task_ids:
                    cursor.execute("""
                                        UPDATE task SET status=%s WHERE id IN %s
                                    """, ('old', tuple(task_ids)))  # Преобразуем список в кортеж


            conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()
