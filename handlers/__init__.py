from aiogram import Router

from .cource import router as course_router

from .payment import router as payment_router
from .referral import router as referral_router
from .start import router as start_router
from .support import router as support_router

router = Router()


router.include_routers(
    start_router, # Старт
    referral_router, # Реферальная система
    support_router, # Поддержка
    payment_router, # Система оплаты
    course_router # Курсы
)

__all__ = [
    'router'
]