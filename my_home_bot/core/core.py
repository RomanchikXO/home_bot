from database.DataBase import *
import psycopg2.extras
from config_data.config import cipher
import time
from datetime import datetime, timedelta


def check_or_add_user(tg_id: int):
    """
    Проверяет наличие пользователя в таблице accounts по tg_id.
    Если пользователь существует, возвращает его данные.
    Если пользователя нет, добавляет нового пользователя и возвращает его данные.

    :param tg_id: Telegram ID пользователя
    :return: словарь с данными пользователя
    """
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        # Проверяем, существует ли пользователь
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM accounts WHERE tg_id = %s", (tg_id,))
            user = cursor.fetchone()

            if user:
                # Если пользователь найден, возвращаем его данные
                return dict(user)  # user уже является словарем
            else:
                # Если пользователя нет, добавляем его
                new_user = add_user(tg_id)
                return new_user

    except Exception as e:
        print(f"Ошибка при проверке или добавлении пользователя: {e}")
        return None
    finally:
        close_connection(conn)


def add_user(tg_id):
    """
    Добавляет нового пользователя в таблицу accounts.

    :param tg_id: Telegram ID пользователя
    :return: словарь с данными нового пользователя
    """
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            cursor.execute(
                "INSERT INTO accounts (tg_id, permissions, states) VALUES (%s, %s, %s) RETURNING *",  # Возвращаем все поля
                (tg_id, 'user', 'new_user')
            )
            new_user = cursor.fetchone()
            conn.commit()  # Сохраняем изменения

            # Возвращаем данные нового пользователя (это уже словарь)
            return dict(new_user)

    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return None
    finally:
        close_connection(conn)


def change_user(tg_id, type:str, text:str):
    """
    изменяет пользователя.

    :param tg_id: Telegram ID пользователя
    """
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        sql = f"UPDATE accounts SET {type} = %s WHERE tg_id = %s"
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            cursor.execute(
                sql,(text, tg_id)
            )
            conn.commit()  # Сохраняем изменения

    except Exception as e:
        print(f"Ошибка изменения пользователя: {e}")
        return None
    finally:
        close_connection(conn)


def get_budget_by_id(budget_id=False, name=False):
    """
    Получает базу бюджета по его ID.

    :param budget_id: ID бюджета
    :return: словарь с данными бюджета или None, если бюджет не найден
    """
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        sql = f"SELECT * FROM budgets"
        params = ()
        if budget_id:
            sql += f" WHERE id = %s"
            params = (budget_id,)
        if name:
            sql += f" WHERE name = %s"
            params = (name,)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql, params)
            budget = cursor.fetchall()
            if budget:
                result = [{key: row[key] for key in row.keys() if key in ['id', 'name', 'pass']} for row in budget]
            else:
                result = None

            return result

    except Exception as e:
        print(f"Ошибка при получении бюджета: {e}")
        return None
    finally:
        close_connection(conn)


def create_budgets(name:str, new_pass:str, tg_id:int):
    # создать запись в budgets
    # перезаписать у пользователя
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            cursor.execute(
                "INSERT INTO budgets (name, pass) VALUES (%s, %s) RETURNING id",
                (name, new_pass)
            )
            new_id = cursor.fetchone()['id']
            conn.commit()
            change_user(tg_id, type='budget_id', text=new_id)

    except Exception as e:
        print(f"Ошибка при создании категории: {e}")
        return None
    finally:
        close_connection(conn)


def get_categories(id_budgets:int, type:str):
    # получить категории
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("SELECT * "
                           "FROM categories "
                           "WHERE id_budget = %s"
                           "AND  type=%s", (id_budgets, type,))
            cats = cursor.fetchall()
            result = [{key: row[key] for key in row.keys() if key in ['category']} for row in cats]
            return result  # Возвращаем данные бюджета в виде словаря

    except Exception as e:
        print(f"Ошибка при получения категорий: {e}")
        return None
    finally:
        close_connection(conn)


def create_cat(cat_name:str, type:str, id_budget:int):
    # создать категории
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            cursor.execute(
                "INSERT INTO categories (category, type, id_budget) VALUES (%s, %s, %s)",
                (cat_name, type, id_budget)
            )
            conn.commit()

    except Exception as e:
        print(f"Ошибка при создании категории: {e}")
        return None
    finally:
        close_connection(conn)



def encrypt_password(password: str) -> str:
    """Шифрует пароль"""
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password: str) -> str:
    """Расшифровывает пароль"""
    decrypted_password = cipher.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

def handle_password(new_password: str, old_password: str = None) -> str:
    """
    Проверяет пароли на совпадение

    :param new_password: Новый пароль или зашифрованный пароль
    :param old_password: Зашифрованный старый пароль (необязательный)
    :return: Зашифрованный новый пароль или сообщение о совпадении
    """

    if old_password:
        try:
            decrypted_old_password = decrypt_password(old_password)
            if decrypted_old_password == new_password:
                return True
            else:
                return False
        except Exception as e:
            return f"Ошибка при расшифровке старого пароля: {e}"
    else:
        return "Старый пароль не передан."


def money_move_change(new_sum:float, cat:str, cat_name:str, id_user:int, id_budg:int, comm):
    # добавить запись в money_move
    # cat - это название столбца (income: доход / expenditure: расход)
    # cat_name - это название категории
    # comm - комментарий
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            sql = f"INSERT INTO money_move (category, {cat}, id_user, id_budgets, comment) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(
                sql,(cat_name, new_sum, id_user, id_budg, comm,)
            )
            conn.commit()

    except Exception as e:
        print(f"Ошибка добавлении записи в money_move: {e}")
        return None
    finally:
        close_connection(conn)


def money_move_select(id_budgets: int, id : int = False):
    # вытянут записи из money_move
    # id_budgets - это id базы
    # id - это id в базе

    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            sql = f"SELECT * FROM money_move WHERE id_budgets = %s AND date_add >= %s"
            params = (id_budgets, get_first_day_of_month())
            if id:
                sql = f"SELECT * FROM money_move WHERE id_budgets = %s AND id = %s"
                params = (id_budgets, id,)

            cursor.execute(
                sql,(params)
            )

            data = cursor.fetchall()
            result = [{key: row[key] for key in row.keys() if key in ['category', 'income', 'expenditure', 'id_user',
                                                                      'id_budgets', 'date_add', 'comment']} for row in
                      data]
            return result


    except Exception as e:
        print(f"Ошибка добавлении записи в money_move: {e}")
        return None
    finally:
        close_connection(conn)


def get_history_for_user(id_budgets, offset=0, limit=10):
    """
    Получает `limit` записей из таблицы money_move для одной группы пользователей `id_budgets`,
    начиная с `offset`, отсортированные по дате добавления (date_add) в порядке убывания.
    """

    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql =  """SELECT category, income, expenditure, comment, id, id_user FROM money_move WHERE id_budgets = %s ORDER BY date_add DESC OFFSET %s LIMIT %s;"""
            params = (id_budgets, offset, limit)
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            result = [
                {'category': row['category'], 'income': row['income'], 'expenditure': row['expenditure'],
                 'comment': row['comment'], 'id' : row['id'], 'id_user': row['id_user']}
                for row in rows
            ]
            return result


    except Exception as e:
        print(f"Ошибка получения 10 записей в money_move: {e}")
        return None
    finally:
        close_connection(conn)


def count_records(id_budgets):
    """
    Возвращает общее количество записей в таблице money_move для группы `id_budgets`.
    """
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = "SELECT COUNT(*) FROM money_move WHERE id_budgets = %s;"
            params = (id_budgets,)

            cursor.execute(sql, params)
            count_row = cursor.fetchone()
            count = count_row['count'] if count_row else 0
            return count

    except Exception as e:
        print(f"Ошибка получения кол-ва записей в money_move для группы {id_budgets}: {e}")
        return None
    finally:
        close_connection(conn)


def del_or_edit_task (type_but:str, id_record:int, new_sum=False):
    """
    удалить или изменить запись в money move
    """
    sql = ''
    conn = connect_to_database()
    if not conn:
        return None
    if type_but == 'del':
        sql = f"DELETE FROM money_move WHERE id = %s"
        params = (id_record,)
    elif type_but == 'edit':
        sql = """
        UPDATE money_move SET income = CASE WHEN income = 0 THEN income ELSE %s END, expenditure = CASE WHEN income = 0 THEN %s ELSE expenditure END WHERE id = %s
        """
        params = (new_sum, new_sum, id_record)
    else:
        # Если тип операции не поддерживается
        print("Некорректный тип операции")
        return None


    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql, params)
            conn.commit()
    except Exception as e:
        print(f"Ошибка при обновлении/удалении записи в money_move: {e}")
        return None
    finally:
        close_connection(conn)



def get_tasks(id_user, date_start=False, status=False, id_task=False):
    # выгрузить все задачи пользователя
    conn = connect_to_database()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            params = (id_user,)
            sql = f"SELECT * FROM task WHERE id_user = %s"
            if id_task:
                sql += f" AND id=%s"
                params += (id_task,)

            sql += " ORDER BY plane_date ASC"
            cursor.execute(sql, params)
            tasks = cursor.fetchall()
            result = [{key: row[key] for key in row.keys() if key in ['id', 'task', 'plane_date', 'status']} for row in tasks]
            return result  # Возвращаем данные бюджета в виде словаря

    except Exception as e:
        print(f"Ошибка при выгрузке задач: {e}")
        return None
    finally:
        close_connection(conn)


def add_task(id_user:int, text:str, plane_date:int, status='new'):
    """
    добавить новую задачу в task
    plane_date: дата 23:59:00 UNIX

    """
    conn = connect_to_database()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = "INSERT INTO task (id_user, task, status, plane_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql,(id_user, text, status, plane_date)
            )
            conn.commit()

    except Exception as e:
        print(f"Ошибка добавлении записи в task: {e}")
        return None
    finally:
        close_connection(conn)


def delete_task(id_task:int):
    """
    Удалить задачу
    id_task id задачи в базе task
    """
    conn = connect_to_database()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = "DELETE FROM task WHERE id=%s"
            cursor.execute(
                sql, (id_task,)
            )
            conn.commit()

    except Exception as e:
        print(f"Ошибка удаления записи в task: {e}")
        return None
    finally:
        close_connection(conn)


def convert_unix_time(unix_time: int, format_string: str):
    """
    Преобразует UNIX-время в строку в указанном формате.

    Аргументы:
    ----------
    unix_time : int
        Время в формате UNIX (в секундах с 01.01.1970).
    format_string : str
        Формат, в который нужно преобразовать время. Используются следующие обозначения:
        - %Y: год (4 цифры)
        - %m: месяц (2 цифры)
        - %d: день (2 цифры)
        - %H: часы (24 часа)
        - %M: минуты
        - %S: секунды

    Возвращает:
    -----------
    str:
        Строка, отформатированная в соответствии с переданным шаблоном.

    Примеры форматов:
    -----------------
    - 'гггг.мм.дд' -> '%Y.%m.%d'
    - 'дд.мм.гггг' -> '%d.%m.%Y'
    - 'чч:мм:сс' -> '%H:%M:%S'
    - 'дд.мм.гггг чч:мм' -> '%d.%m.%Y %H:%M'
    """
    dt_object = datetime.utcfromtimestamp(unix_time)

    # Заменяем псевдоформаты на реальные для strftime
    format_string = format_string.replace('гггг', '%Y').replace('мм', '%m').replace('дд', '%d')
    format_string = format_string.replace('чч', '%H').replace('мм', '%M').replace('сс', '%S')

    return dt_object.strftime(format_string)


def convert_to_unix(date_str):
    """
    перевести дату в формате dd.mm.yyyy в UNIX
    """
    return int(time.mktime(datetime.strptime(date_str, "%d.%m.%Y").replace(hour=23, minute=59, second=0).timetuple()))


def get_first_day_of_month():
    """получить первый день месяца UNIX"""
    now = datetime.utcnow() + timedelta(hours=3)
    first_day = datetime(year=now.year, month=now.month, day=1, hour=0, minute=1)
    unix_timestamp = int(time.mktime(first_day.timetuple()))
    return unix_timestamp


def get_piggy(id_budg):
    # получить сумму копилки
    conn = connect_to_database()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = f"SELECT * FROM piggy WHERE budget_id = %s"
            cursor.execute(sql, (id_budg,))
            records = cursor.fetchall()
            result = [{key: row[key] for key in row.keys() if key in ['id', 'money', 'time_add', 'status']} for row in records]
            return result  # Возвращаем данные бюджета в виде словаря

    except Exception as e:
        print(f"Ошибка при выгрузке копилки: {e}")
        return None
    finally:
        close_connection(conn)


def edit_piggy(money:float, id_budg:int, status:str):
    # добавить / убавить из копилки
    conn = connect_to_database()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = f"INSERT INTO piggy (money, budget_id, status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (money, id_budg, status,))
            conn.commit()

    except Exception as e:
        print(f"Ошибка при добавлении в копилку: {e}")
        return None
    finally:
        close_connection(conn)


def get_unix_to_day():
    # сегодня в 23:59 unix (по мск)

    # Получаем текущее время
    now = datetime.utcnow()

    # Устанавливаем временную зону на Московское время (UTC+3)
    moscow_time = now + timedelta(hours=3)

    # Устанавливаем время на 23:59
    moscow_time = moscow_time.replace(hour=23, minute=59, second=0, microsecond=0)

    # Возвращаем время в формате Unix timestamp
    return int(moscow_time.timestamp())

