import os
from dotenv import load_dotenv, find_dotenv
from cryptography.fernet import Fernet


env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')



if not os.path.exists(env_path):
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv(env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    exit("BOT_TOKEN не найден в переменных окружения.")



# Проверяем наличие ключа в .env
KEY = os.getenv("KEY")
if not KEY:
    key = Fernet.generate_key()
    # Записываем новый ключ в файл .env на уровень выше
    with open(env_path, 'a') as f:
        f.write(f"KEY={key.decode()}\n")
else:
    key = KEY.encode()

cipher = Fernet(key)



DEFAULT_COMMANDS = [
    ("/start", "Начать работу с ботом")
]