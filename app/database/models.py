from logger import logger

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime


# Создаём базовый класс для моделей SQLAlchemy
class Base(DeclarativeBase):
    pass

# Пользователи и профили
class User(Base):
    """Пользователь Telegram-бота."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор пользователя в базе
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  # Telegram ID пользователя (например, 123456789)
    first_name: Mapped[str | None] = mapped_column(String(64))  # Имя пользователя из Telegram (например, "Иван")
    last_name: Mapped[str | None] = mapped_column(String(64))  # Фамилия пользователя из Telegram (например, "Иванов")
    username: Mapped[str | None] = mapped_column(String(32))  # Никнейм пользователя из Telegram (например, "@ivanov")
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)  # Признак подписки (Telegram Premium)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)  # Забанен ли пользователь админом (True/False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)  # Заблокировал ли пользователь бота (True/False)
    language_code: Mapped[str | None] = mapped_column(String(10), default="ru")  # Язык Telegram клиента (например, "ru", "en")
    last_active: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))  # Время последней активности (например, 2025-05-17 22:00:00+03)
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # Согласие на обработку персональных данных
    consent_date: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # Дата и время согласия
    consent_version: Mapped[str | None] = mapped_column(String(20), nullable=True)  # Версия соглашения (например, "1.0")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # Время создания записи
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Время последнего обновления

    # Отношения
    profile: Mapped["UserProfile"] = relationship(back_populates="user")  # Профиль пользователя (1:1)
    subscription: Mapped["Subscription"] = relationship(back_populates="user")  # Активная подписка (1:1)
    usage_limits: Mapped[list["UsageLimit"]] = relationship(back_populates="user")  # Лимиты генерации гороскопов (1:N)
    horoscopes: Mapped[list["Horoscope"]] = relationship(back_populates="user")  # Кэшированные гороскопы (1:N)
    notification_settings: Mapped[list["NotificationSetting"]] = relationship(back_populates="user")  # Настройки уведомлений (1:N)
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")  # История уведомлений (1:N)
    payments: Mapped[list["Payment"]] = relationship(back_populates="user")  # История платежей (1:N)


class UserProfile(Base):
    """Профиль пользователя с данными для гороскопов и уведомлений."""
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор профиля
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Ссылка на пользователя (id из users)
    city_name: Mapped[str | None] = mapped_column(String(100))  # Название города проживания из GeoNames API (например, "Москва")
    city_timezone: Mapped[str | None] = mapped_column(String(32))  # Часовой пояс города проживания (например, "Europe/Moscow")
    birth_date: Mapped[Date | None] = mapped_column(Date)  # Дата рождения для гороскопа (например, 1990-01-01)
    birth_time: Mapped[Time | None] = mapped_column(Time)  # Время рождения для гороскопа (например, 14:30)
    birth_city_name: Mapped[str | None] = mapped_column(String(100))  # Название города рождения из GeoNames API (например, "Козловка")
    birth_latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))  # Широта города рождения (например, 56.123400)
    birth_longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))  # Долгота города рождения (например, 35.567800)
    birth_timezone: Mapped[str | None] = mapped_column(String(32))  # Часовой пояс города рождения (например, "Europe/Moscow")
    gender: Mapped[str | None] = mapped_column(String(20))  # Пол для гороскопа (например, "male", "female", "other")
    zodiac_sign: Mapped[str | None] = mapped_column(String(20))  # Знак зодиака (например, "Aries")

    # Отношения
    user: Mapped["User"] = relationship(back_populates="profile")  # Ссылка на пользователя (1:1)



# Подписки
class SubscriptionType(Base):
    """Тип подписки с лимитами."""
    __tablename__ = "subscription_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор типа подписки
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # Название подписки (например, "Free", "Glow")
    description: Mapped[str | None] = mapped_column(Text)  # Описание подписки (например, "5 гороскопов в день")
    price: Mapped[float | None] = mapped_column(Numeric(10, 2))  # Цена подписки (например, 499.00)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)  # Длительность подписки в днях (например, 30)
    limits: Mapped[dict | None] = mapped_column(JSONB)  # Лимиты в формате JSON (например, {"daily_horoscopes": 5})

    # Отношения
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="subscription_type")  # Подписки этого типа (1:N)


class Subscription(Base):
    """Активная подписка пользователя."""
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор подписки
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Ссылка на пользователя
    subscription_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscription_types.id"), nullable=False)  # Ссылка на тип подписки
    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)  # Дата начала подписки
    end_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)  # Дата окончания подписки
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=False)  # Автопродление подписки (True/False)
    status: Mapped[str] = mapped_column(String(20), default="active")  # Статус подписки (например, "active", "expired")
    payment_id: Mapped[str | None] = mapped_column(String(100))  # ID платежа из ЮKassa (например, "12345-67890")
    payment_method_id: Mapped[str | None] = mapped_column(String(100))  # ID метода оплаты из ЮKassa
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # Время создания
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Время обновления

    # Отношения
    user: Mapped["User"] = relationship(back_populates="subscription")  # Ссылка на пользователя (1:1)
    subscription_type: Mapped["SubscriptionType"] = relationship(back_populates="subscriptions")  # Ссылка на тип подписки (M:1)
    payments: Mapped[list["Payment"]] = relationship(back_populates="subscription")  # Платежи для подписки (1:N)



# Гороскопы и лимиты
class UsageLimit(Base):
    """Лимиты генерации гороскопов."""
    __tablename__ = "usage_limits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор записи
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    date: Mapped[Date] = mapped_column(Date, nullable=False)  # Дата лимита (например, 2025-05-17)
    horoscope_count: Mapped[int] = mapped_column(Integer, default=0)  # Количество сгенерированных гороскопов за день
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # Время создания
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Время обновления

    # Отношения
    user: Mapped["User"] = relationship(back_populates="usage_limits")  # Ссылка на пользователя (M:1)


class Horoscope(Base):
    """Кэшированный персонализированный гороскоп."""
    __tablename__ = "horoscopes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор гороскопа
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    date: Mapped[Date] = mapped_column(Date, nullable=False)  # Дата гороскопа (например, 2025-05-17)
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Текст гороскопа от Free Astrology API
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # Время создания

    # Отношения
    user: Mapped["User"] = relationship(back_populates="horoscopes")  # Ссылка на пользователя (M:1)



# Уведомления
class NotificationSetting(Base):
    """Настройки уведомлений пользователя."""
    __tablename__ = "notification_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор настройки
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Тип уведомления (например, "horoscope")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)  # Включено ли уведомление (True/False)
    preferred_time: Mapped[Time | None] = mapped_column(Time)  # Предпочитаемое время уведомления (например, 08:00)
    frequency: Mapped[str | None] = mapped_column(String(20), default="daily")  # Частота (например, "daily", "weekly")

    # Отношения
    user: Mapped["User"] = relationship(back_populates="notification_settings")  # Ссылка на пользователя (M:1)


class Notification(Base):
    """История отправленных уведомлений."""
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор уведомления
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Тип уведомления (например, "horoscope")
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # Время отправки
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # Статус (например, "sent", "failed")

    # Отношения
    user: Mapped["User"] = relationship(back_populates="notifications")  # Ссылка на пользователя (M:1)



# Платежи
class Payment(Base):
    """История платежей через ЮKassa."""
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Уникальный идентификатор платежа
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Ссылка на пользователя
    subscription_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("subscriptions.id"))  # Ссылка на подписку (может быть NULL)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # Сумма платежа (например, 499.00)
    payment_id: Mapped[str] = mapped_column(String(100), nullable=False)  # ID платежа из ЮKassa (например, "12345-67890")
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # Статус платежа (например, "succeeded", "pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # Время создания

    # Отношения
    user: Mapped["User"] = relationship(back_populates="payments")  # Ссылка на пользователя (M:1)
    subscription: Mapped["Subscription"] = relationship(back_populates="payments")  # Ссылка на подписку (M:1, опционально)



# Для отладки: проверяем зарегистрированные таблицы
logger.info(f"Registered tables: {Base.metadata.tables.keys()}")