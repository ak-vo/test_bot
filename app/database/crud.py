# Операции с БД (CRUD)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User

# Добавление пользователя в БД
async def add_user(session: AsyncSession, user_id: int, name: str):
    # Проверяем, есть ли пользователь
    user = await session.get(User, user_id)
    if not user:
        # Если нет, создаём нового
        user = User(user_id=user_id, name=name)
        session.add(user)
        await session.commit()