from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models import User, UserProfile
from typing import Optional

async def add_or_update_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
    is_premium: Optional[bool] = False
) -> User:
    """
    Добавляет нового пользователя или обновляет существующего, создаёт профиль.

    Args:
        session: Асинхронная сессия SQLAlchemy.
        telegram_id: Telegram ID пользователя.
        first_name: Имя пользователя.
        last_name: Фамилия пользователя.
        username: Никнейм пользователя.

    Returns:
        User: Объект пользователя (новый или обновлённый).
    """
    async with session.begin():
        # Проверяем, существует ли пользователь
        user = await session.scalar(
            select(User).filter_by(telegram_id=telegram_id)
        )

        if user:
            # Обновляем данные
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.is_premium = is_premium or False
            user.last_active = func.now()
            user.updated_at = func.now()
        else:
            # Создаём нового пользователя
            user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                is_premium=is_premium or False,
                is_banned=False,
                is_blocked=False,
                language_code="ru",
                last_active=func.now(),
                created_at=func.now(),
                updated_at=func.now()
            )
            session.add(user)
            await session.flush()  # Получаем user.id

            # Создаём профиль
            profile = UserProfile(user_id=user.id)
            session.add(profile)

        await session.commit()
        return user