"""Create initial tables

Revision ID: e07d53dd2544
Revises: 
Create Date: 2025-05-18 18:12:44.978790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = 'e07d53dd2544'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Обновить схему."""
    # Создание таблицы users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор пользователя
        sa.Column('telegram_id', sa.BigInteger, nullable=False, unique=True),  # Telegram ID пользователя
        sa.Column('first_name', sa.String(64), nullable=True),  # Имя пользователя из Telegram
        sa.Column('last_name', sa.String(64), nullable=True),  # Фамилия пользователя из Telegram
        sa.Column('username', sa.String(32), nullable=True),  # Никнейм пользователя из Telegram (@username)
        sa.Column('is_premium', sa.Boolean, server_default=sa.false(), nullable=False),  # Признак подписки (Telegram Premium)
        sa.Column('is_banned', sa.Boolean, server_default=sa.false(), nullable=False),  # Забанен ли пользователь
        sa.Column('is_blocked', sa.Boolean, server_default=sa.false(), nullable=False),  # Заблокировал ли бот
        sa.Column('language_code', sa.String(10), server_default='ru', nullable=True),  # Код языка (ru, en)
        sa.Column('last_active', sa.DateTime(timezone=True), nullable=True),  # Время последней активности
        sa.Column('consent_given', sa.Boolean, server_default=sa.false(), nullable=False),  # Согласие на обработку персональных данных
        sa.Column('consent_date', sa.DateTime(timezone=True), nullable=True),  # Дата и время согласия
        sa.Column('consent_version', sa.String(20), nullable=True), # Версия соглашения (например, "1.0")
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),  # Время создания
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)  # Время обновления
    )
    op.create_index('idx_users_telegram_id', 'users', ['telegram_id'])

    # Создание таблицы user_profiles
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор профиля
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),  # Ссылка на пользователя
        sa.Column('city_name', sa.String(100), nullable=True),  # Название города проживания (из GeoNames API)
        sa.Column('city_timezone', sa.String(32), nullable=True),  # Часовой пояс города проживания (например, Europe/Moscow)
        sa.Column('birth_date', sa.Date, nullable=True),  # Дата рождения (например, 1990-01-01)
        sa.Column('birth_time', sa.Time, nullable=True),  # Время рождения (например, 14:30)
        sa.Column('birth_city_name', sa.String(100), nullable=True),  # Название города рождения (из GeoNames API)
        sa.Column('birth_latitude', sa.Numeric(9, 6), nullable=True),  # Широта города рождения
        sa.Column('birth_longitude', sa.Numeric(9, 6), nullable=True),  # Долгота города рождения
        sa.Column('birth_timezone', sa.String(32), nullable=True),  # Часовой пояс города рождения
        sa.Column('gender', sa.String(20), nullable=True),  # Пол (male, female, other)
        sa.Column('zodiac_sign', sa.String(20), nullable=True)  # Знак зодиака (например, Aries)
    )
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'])

    # Создание таблицы subscription_types
    op.create_table(
        'subscription_types',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор типа подписки
        sa.Column('name', sa.String(50), nullable=False),  # Название подписки (Free, Glow, Glow Up)
        sa.Column('description', sa.Text, nullable=True),  # Описание подписки
        sa.Column('price', sa.Numeric(10, 2), nullable=True),  # Цена подписки (например, 499.00)
        sa.Column('duration_days', sa.Integer, nullable=False),  # Длительность подписки в днях
        sa.Column('limits', JSONB, nullable=True)  # Лимиты (например, {"daily_horoscopes": 5})
    )

    # Создание таблицы subscriptions
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор подписки
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),  # Ссылка на пользователя
        sa.Column('subscription_type_id', sa.Integer, sa.ForeignKey('subscription_types.id'), nullable=False),  # Ссылка на тип подписки
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),  # Дата начала подписки
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),  # Дата окончания подписки
        sa.Column('auto_renew', sa.Boolean, server_default=sa.false(), nullable=False),  # Автопродление подписки
        sa.Column('status', sa.String(20), server_default='active', nullable=False),  # Статус (active, expired)
        sa.Column('payment_id', sa.String(100), nullable=True),  # ID платежа из ЮKassa
        sa.Column('payment_method_id', sa.String(100), nullable=True),  # ID метода оплаты
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),  # Время создания
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)  # Время обновления
    )
    op.create_index('idx_subscriptions_user_id_status', 'subscriptions', ['user_id', 'status'])

    # Создание таблицы usage_limits
    op.create_table(
        'usage_limits',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор записи
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),  # Ссылка на пользователя
        sa.Column('date', sa.Date, nullable=False),  # Дата лимита (например, 2025-05-17)
        sa.Column('horoscope_count', sa.Integer, server_default='0', nullable=False),  # Количество сгенерированных гороскопов
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),  # Время создания
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)  # Время обновления
    )
    op.create_index('idx_usage_limits_user_id_date', 'usage_limits', ['user_id', 'date'])
    op.create_index('idx_usage_limits_user_id_date_unique', 'usage_limits', ['user_id', 'date'], unique=True)

    # Создание таблицы horoscopes
    op.create_table(
        'horoscopes',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор гороскопа
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),  # Ссылка на пользователя
        sa.Column('date', sa.Date, nullable=False),  # Дата гороскопа (например, 2025-05-17)
        sa.Column('content', sa.Text, nullable=False),  # Текст гороскопа от Free Astrology API
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)  # Время создания
    )
    op.create_index('idx_horoscopes_user_id_date', 'horoscopes', ['user_id', 'date'])

    # Создание таблицы notification_settings
    op.create_table(
        'notification_settings',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор настройки
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),  # Ссылка на пользователя
        sa.Column('notification_type', sa.String(50), nullable=False),  # Тип уведомления (horoscope, affirmation)
        sa.Column('is_enabled', sa.Boolean, server_default=sa.true(), nullable=False),  # Включено ли уведомление
        sa.Column('preferred_time', sa.Time, nullable=True),  # Предпочитаемое время (например, 08:00)
        sa.Column('frequency', sa.String(20), server_default='daily', nullable=True)  # Частота (daily, weekly)
    )
    op.create_index('idx_notification_settings_user_id_type', 'notification_settings', ['user_id', 'notification_type'])

    # Создание таблицы notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор уведомления
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),  # Ссылка на пользователя
        sa.Column('notification_type', sa.String(50), nullable=False),  # Тип уведомления (horoscope, affirmation)
        sa.Column('sent_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),  # Время отправки
        sa.Column('status', sa.String(20), nullable=False)  # Статус (sent, failed)
    )
    op.create_index('idx_notifications_user_id', 'notifications', ['user_id'])

    # Создание таблицы payments
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer, primary_key=True),  # Уникальный идентификатор платежа
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),  # Ссылка на пользователя
        sa.Column('subscription_id', sa.Integer, sa.ForeignKey('subscriptions.id', ondelete='SET NULL'), nullable=True),  # Ссылка на подписку
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),  # Сумма платежа (например, 499.00)
        sa.Column('payment_id', sa.String(100), nullable=False),  # ID платежа из ЮKassa
        sa.Column('status', sa.String(20), nullable=False),  # Статус (succeeded, pending, canceled)
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)  # Время создания
    )
    op.create_index('idx_payments_user_id', 'payments', ['user_id'])



def downgrade() -> None:
    """Откатить схему."""
    # Удаление таблиц в обратном порядке
    op.drop_table('payments')
    op.drop_table('notifications')
    op.drop_table('notification_settings')
    op.drop_table('horoscopes')
    op.drop_table('usage_limits')
    op.drop_table('subscriptions')
    op.drop_table('subscription_types')
    op.drop_table('user_profiles')
    op.drop_table('users')