# Загружаем переменные окружения из .env
from dotenv import load_dotenv
import os

# Инициализируем загрузку .env
load_dotenv()

# Токен бота из BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройки PostgreSQL
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# API внешние
GIGA_CHAT = os.getenv("GIGA_CHAT")
FREE_ASTROLOGY = os.getenv("FREE_ASTROLOGY")
GOOGLE_CUSTOM_SEARCH = os.getenv("GOOGLE_CUSTOM_SEARCH")