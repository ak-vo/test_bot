from aiogram import Router, types
from aiogram.filters import Command

router_profile = Router()

@router_profile.message(Command('account'))
async def handle_account(message: types.Message):
  username = message.from_user.username
  await message.answer(
        f"Привет {username or 'друг'}! Это твой бот. Выбери раздел:"
    )