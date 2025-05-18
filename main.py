# Точка входа бота
from logger import logger

import asyncio
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.handlers.start import router
from app.handlers.profile import router_profile

from app.middlewares.db_session import DatabaseSessionMiddleware
from app.database.db import async_session  # Импортируем фабрику сессий

# Основная функция запуска бота
async def main():
    logger.info("Запуск бота")
    try:
      bot = Bot(token=BOT_TOKEN)
      dp = Dispatcher()
      dp.update.middleware(DatabaseSessionMiddleware(async_session))  # Регистрация middleware
      dp.include_router(router)
      dp.include_router(router_profile)
      await bot.delete_webhook(drop_pending_updates=True)  # Очистим очередь и удалим webhook на всякий случай
      await dp.start_polling(bot, drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {str(e)}")
        raise

# Запуск программы
if __name__ == "__main__":
    try:
      asyncio.run(main())
    except KeyboardInterrupt:
      logger.warning("Программа была остановлена пользователем (KeyboardInterrupt)")
    except Exception as e:
      logger.error(f"Программа завершена с ошибкой: {str(e)}")