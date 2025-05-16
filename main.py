# Точка входа бота
from logger import logger

import asyncio
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.handlers.start import router


# Основная функция запуска бота
async def main():
    logger.info("Старт")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

# Запуск программы
if __name__ == "__main__":
    try:
      asyncio.run(main())
    except:
      logger.info("Конец")