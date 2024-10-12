# CopyTrading Bot

## Перед запуском

1. **Установить зависимости**  
   Убедитесь, что у вас установлен Python 3 и pip. Выполните следующую команду для установки необходимых библиотек:

   ```bash
   pip install -r requirements.txt

2. **создать файл .env c содержимым**
    ```bash
   BOT_TOKEN = "ваш токен"
3. **в папке database создаем файл DataBase.py с содержимым:**
    ```bash
   
    import psycopg2


    DATABASE_CONFIG = {
        'dbname': 'имя базы',
        'user': 'логин',
        'password': 'пароль',
        'host': 'localhost',
        'port': 5432,
    }

    def connect_to_database():
        try:
            conn = psycopg2.connect(**DATABASE_CONFIG)
            return conn
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def close_connection(conn):
        if conn:
            conn.close()
   
4. **Запустить файл main.py**
