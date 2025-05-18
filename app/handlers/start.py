from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import add_or_update_user
from app.keyboards.main_menu import get_main_menu, get_energy_day_menu

router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message, session: AsyncSession):
    # Извлекаем данные пользователя
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    # Добавляем или обновляем пользователя
    await add_or_update_user(
        session=session,
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        username=username
    )

    # Отправляем приветственное сообщение
    await message.answer(
        f"Привет {username or 'друг'}! Это твой бот. Выбери раздел:",
        reply_markup=get_main_menu()
    )