from uuid import uuid4

from datetime import datetime, timezone

from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, Text, ForeignKey, Date, Boolean
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship

from database.db import Base, DATABASE_URL


# Таблица Пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    # Телеграм Айди
    telegram_id = Column(Integer, nullable=False, unique=True)
    # Телеграм Ник
    user_name = Column(String(100), nullable=True)
    # Дата регистрации
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))
    # Реферальная привязка
    referral_id = Column(Integer, nullable=True, default=None)
    # Баланс Пользователя
    balance = Column(Integer, nullable=False, default=0)
    # Связь с таблицей подписки
    subscriptions = relationship("Subscriptions", back_populates="user", cascade="all, delete",
                                 primaryjoin="User.telegram_id==Subscriptions.telegram_id")
    # Связь платежей
    payments = relationship("Payments", back_populates="user", cascade="all, delete",
                            primaryjoin="User.telegram_id==Payments.telegram_id")

# Таблица подписок
class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    # Телеграм айди для привязки к подписке
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    # Дата покупки
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))
    # Тариф
    plan  = Column(String(50), nullable=True)
    # Количество дней подписки
    day_count = Column(Integer, nullable=False)
    # Число дня
    day = Column(Integer, nullable=False)
    # Число Месяца
    month = Column(Integer, nullable=False)
    # Год
    year = Column(Integer, nullable=False)
    # Связка с Телеграм Айди Пользователя
    user = relationship("User", back_populates="subscriptions",
                        primaryjoin="Subscriptions.telegram_id==User.telegram_id")



    # Получение Тарифов информации о тарифах
    @staticmethod
    def get_plans():
        return {
            'none': 'Отсутствие тарифа',
            'base': 'Базовый Тариф',
            'advanced': 'Средний Тариф',
            'exclusive': 'Эксклюзивный тариф',
            'all': 'Тариф на все'
        }

# Таблица Платежей
class Payments(Base):
    __tablename__ = 'payments'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    # Телеграм айди для привязки
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    # Дата покупки
    registered_at = Column(DateTime, default=datetime.now(timezone.utc))
    # Тариф
    plan = Column(String(50), nullable=False)
    # Количество дней подписки
    day_count = Column(Integer, nullable=False)
    # Внесенная сумма оплаты
    pay_sum = Column(Integer, nullable=False)
    # Число дня
    day = Column(Integer, nullable=False)
    # Число Месяца
    month = Column(Integer, nullable=False)
    # Год
    year = Column(Integer, nullable=False)
    # Связка с Телеграм Айди Пользователя
    user = relationship("User", back_populates="payments",
                        primaryjoin="Payments.telegram_id==User.telegram_id")


# class Video(Base):
#     __tablename__ = 'subscriptions'
#     id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
#
