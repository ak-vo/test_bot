import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Создаём директорию для логов, если не существует
os.makedirs("logs", exist_ok=True)

# Настройка обработчика с ежедневной ротацией
handler = TimedRotatingFileHandler(
    filename="logs/bot.log",
    when="midnight", # Ротация в полночь
    interval=1, # Каждые 1 "when"
    backupCount=7, # Хранить только последние 7 файлов
    encoding="utf-8",
    utc=True # Если хочешь использовать UTC, иначе убери
)

# Формат логов
formatter = logging.Formatter(
    '[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}',
    style='{'
)
handler.setFormatter(formatter)

# Устанавливаем общий логгер
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)