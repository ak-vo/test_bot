# Создание инлайн-клавиатур
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Основное меню
def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Астрология", callback_data="astrology"),
            InlineKeyboardButton(text="Сонник", callback_data="dreambook")
        ]
    ])
    return keyboard

# Меню для раздела "Астрология"
def get_astrology_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Общий гороскоп", callback_data="general_horo"),
            InlineKeyboardButton(text="Персональный гороскоп", callback_data="personal_horo")
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    return keyboard