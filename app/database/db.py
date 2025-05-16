# Настройка асинхронного подключения к PostgreSQL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Формируем URL для подключения к БД
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаём асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL

# Создаём фабрику сессий для работы с БД
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Генератор для получения сессии БД
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session