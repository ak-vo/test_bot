# Создание инлайн-клавиатур
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.dictionary.dictionary import MENU

# Основное меню
def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Энергия дня 🌟", callback_data="energy_day")],
        [InlineKeyboardButton(text="🔮 Интуитивные подсказки 🔮", callback_data="intuitive_hints")],
        [InlineKeyboardButton(text="🧘🏼‍♀️ Практики гармонии 🧘🏻‍♀️", callback_data="harmony_practices")]
    ])
    return keyboard

# Меню для раздела "Энергия дня"
def get_energy_day_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Астрология", callback_data="astrology")],
        [InlineKeyboardButton(text="Натальная карта", callback_data="astrology")],

        [InlineKeyboardButton(text=f"{MENU['Назад']}", callback_data="back_to_main")]
    ])
    return keyboard