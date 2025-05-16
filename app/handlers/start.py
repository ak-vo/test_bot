# Обработчики команд и callback'ов
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.database.crud import add_user
from app.database.db import get_session
from app.keyboards.main_menu import get_main_menu, get_astrology_menu

# Создаём роутер для обработчиков
router = Router()

# Обработка команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    # Добавляем пользователя в БД
    # async for session in get_session():
    #     await add_user(session, message.from_user.id, message.from_user.full_name)
    # Отправляем приветственное сообщение с меню
    await message.answer(
        f"Привет {message.from_user.username}! Это твой бот. Выбери раздел:",
        reply_markup=get_main_menu()
    )

# Обработка нажатий на инлайн-кнопки
@router.callback_query()
async def process_callback(callback: CallbackQuery):
    # Получаем callback_data
    data = callback.data
    # Обрабатываем нажатие на "Астрология"
    if data == "astrology":
        await callback.message.edit_text(
            "Выбери тип гороскопа:",
            reply_markup=get_astrology_menu()
        )
    # Обрабатываем нажатие на "Общий гороскоп"
    elif data == "general_horo":
        await callback.message.edit_text(
            "Здесь будет общий гороскоп (пока заглушка).",
            reply_markup=get_astrology_menu()
        )
    # Обрабатываем нажатие на "Персональный гороскоп"
    elif data == "personal_horo":
        await callback.message.edit_text(
            "Здесь будет персональный гороскоп (пока заглушка).",
            reply_markup=get_astrology_menu()
        )
    # Обрабатываем нажатие на "Назад"
    elif data == "back_to_main":
        await callback.message.edit_text(
            "Выбери раздел:",
            reply_markup=get_main_menu()
        )
    # Подтверждаем обработку callback
    await callback.answer()