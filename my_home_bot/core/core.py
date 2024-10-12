from database.DataBase import *
import psycopg2.extras
from config_data.config import cipher



def check_or_add_user(tg_id):
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


def money_move_change(new_sum:float, cat:str, cat_name:str, id_user:int, id_budg:int):
    # добавить запись в money_move
    # cat - это название столбца (income: доход / expenditure: расход)
    # cat_name - это название категории
    conn = connect_to_database()
    if not conn:
        return None  # Возвращаем None, если не удалось подключиться к базе данных

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # Добавляем нового пользователя в базу данных
            sql = f"INSERT INTO money_move (category, {cat}, id_user, id_budgets) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql,(cat_name, new_sum, id_user, id_budg)
            )
            conn.commit()

    except Exception as e:
        print(f"Ошибка добавлении записи в money_move: {e}")
        return None
    finally:
        close_connection(conn)
